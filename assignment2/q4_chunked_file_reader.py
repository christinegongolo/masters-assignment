"""
Question 4 (20 marks)
Loading a 50GB CSV file directly into RAM causes an OutOfMemoryError.
Create a memory-efficient pipeline using Python generators.

Write a custom generator function chunked_file_reader(file_path, chunk_size_bytes)
that:
  - Opens and reads a text file lazily in chunks of size chunk_size_bytes
    (e.g. 1024 * 1024 for 1MB blocks).
  - Prevents line tearing: lines spanning across chunk boundaries must be
    combined so the generator yields complete, unbroken lines one by one.
  - Keeps peak memory footprint minimal (never loads the whole file with
    .readlines()).

--------------------------------------------------------------------------
Approach
--------------------------------------------------------------------------
We open the file in binary mode and read it chunk_size_bytes at a time.
Each raw chunk is decoded to text and appended to a small "leftover"
buffer. We then split that buffer on newlines: every piece except the
very last is a complete line and can be yielded immediately. The last
piece might be an incomplete line (cut off mid-way by the chunk boundary),
so instead of yielding it, we keep it as the new leftover buffer and
prepend it to the next chunk we read. This is what prevents "line
tearing". At end of file, if there is anything left in the buffer, it is
yielded as the final line.

Only one chunk (plus a small leftover fragment) is ever held in memory
at once, regardless of how large the file is.
"""

import os


def chunked_file_reader(file_path, chunk_size_bytes):
    """
    Generator that lazily yields complete lines from a (potentially huge)
    text file, reading it chunk_size_bytes at a time instead of loading
    the whole file into memory.
    """
    leftover = ""

    with open(file_path, "r", encoding="utf-8", newline="") as f:
        while True:
            chunk = f.read(chunk_size_bytes)
            if not chunk:
                break  # end of file

            # Prepend leftover fragment from the previous chunk
            buffer = leftover + chunk

            # Split into lines; the last element may be incomplete
            lines = buffer.split("\n")

            # Everything except the last piece is a complete line
            for line in lines[:-1]:
                yield line

            # The last piece may be a partial line cut by the chunk
            # boundary (or "" if the chunk ended exactly on a newline) -
            # carry it over to combine with the next chunk.
            leftover = lines[-1]

    # After the loop, yield whatever is left (the final line, which may
    # not have had a trailing newline).
    if leftover:
        yield leftover


def demo():
    # Build a sample file to demonstrate the generator
    sample_path = "sample_large_file.txt"
    with open(sample_path, "w", encoding="utf-8") as f:
        for i in range(1, 1001):
            f.write(f"row {i},value_{i * 2}\n")

    print(f"File size: {os.path.getsize(sample_path)} bytes")

    # Deliberately use a tiny chunk size (64 bytes) so that lines are
    # very likely to be split across chunk boundaries, proving the
    # line-tearing prevention works.
    line_count = 0
    first_few = []
    for line in chunked_file_reader(sample_path, chunk_size_bytes=64):
        line_count += 1
        if line_count <= 5:
            first_few.append(line)

    print("First 5 lines read via generator:")
    for line in first_few:
        print(" ", line)

    print(f"Total lines read: {line_count}")

    # Sanity check against the built-in line reader
    with open(sample_path, "r", encoding="utf-8") as f:
        expected = sum(1 for _ in f)
    assert line_count == expected, "Line count mismatch — possible line tearing!"
    print("No line tearing detected: line counts match.")

    os.remove(sample_path)


if __name__ == "__main__":
    demo()
