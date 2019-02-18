LZ77 Encoder
To run the compression/decompression on a file:
 - In the command line/terminal
 - Traverse to the location of the .py file
 - To compress a file:
   > py lz77.py C File_Name Window Lookahead
   where:
	C is to compress
	File_Name is the path and name of the file to compress
	Window is the bits to store the Window (Recommended 16)
	Lookahead the bits to store the Lookahead (Recommended 8)
 - If this opens Python 2.X (and/or returns error) you may need:
   > python3 lz77.py C File_Name Window Lookahead
 - Max length of the window and lookahead will be 2^X-1, where X is the values chosen
 - To decompress the compressed file:
   > py lz77.py D Compressed_File_Name Window Lookahead
   where:
	D is to decompress
	Compressed_File_Name is the path and name of the file to decompress
	Window is the bits used to store the Window during compression (Recommended 16)
	Lookahead the bits used to store the Lookahead during compression (Recommended 8)
 - If this opens Python 2.X (and/or returns an error) you may need
   > python3 lz77.py D Compressed_File_Name Window Lookahead

Encoding will save the compressed data to a .bin file, and Decoding will save the
decompressed file with the original extension. Compression/Decompression time 
are output, as well as compression ratio. This will also be stored in a results.txt file.