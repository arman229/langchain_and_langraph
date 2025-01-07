### Definitions

1. **ASCII (American Standard Code for Information Interchange)**:
   - **Definition**: ASCII is a character encoding standard that represents text in computers and other devices that use text. It uses **7 bits** to represent characters, allowing for a total of **128 unique characters**. These characters include English letters (both uppercase and lowercase), digits, punctuation marks, and control characters.
   - **Range**: ASCII characters range from `0` to `127` (or `0x00` to `0x7F` in hexadecimal).
   - **Usage**: Primarily used for English text and simple control characters.

2. **Unicode**:
   - **Definition**: Unicode is a comprehensive character encoding standard that aims to represent every character in every language, including emojis and special symbols. It provides a unique **code point** for each character.
   - **Code Points**: Unicode can assign code points to over **1 million characters** (range `0x000000` to `0x10FFFF`).
   - **Purpose**: Unicode enables the global exchange of text in any language, making it essential for modern computing.

---

### How They Are Stored in Computer Memory (Using Different Encodings)

#### 1. **ASCII Storage**:
- **Encoding**: Since ASCII uses only 7 bits per character, it can be stored in a **single byte (8 bits)**. However, only the first 7 bits are used for the character, and the 8th bit is unused.
- **Example**: The character `'A'` in ASCII has the decimal value **65**, which is `01000001` in binary.
- **Memory Storage**: ASCII characters are stored in memory using 1 byte (8 bits), e.g., for `'A'`, `01000001`.

| Character | ASCII Code | Binary Representation | Memory Storage (Hexadecimal) |
|-----------|------------|-----------------------|-----------------------------|
| A         | 65         | 01000001              | 0x41                        |

#### 2. **Unicode Storage** (Using UTF-8, UTF-16, UTF-32 Encodings)

### **UTF-8 Encoding** (Variable-Length Encoding)
- **Definition**: UTF-8 is a variable-length encoding system. It uses **1 to 4 bytes** to represent characters. For characters in the ASCII range (code points `0x0000` to `0x007F`), UTF-8 uses 1 byte, making it backward-compatible with ASCII. For characters outside the ASCII range, it uses 2, 3, or 4 bytes.
- **How It Works**:
  - For code points `0x0000` to `0x007F` (standard ASCII), it uses **1 byte**.
  - For code points `0x0800` to `0xFFFF` (includes most non-ASCII characters), it uses **3 bytes**.
  - For higher code points, it uses **4 bytes**.
  
**Example**: Unicode character `'你'` has the code point `20320` (or `4F60` in hex).
- **Binary for `4F60`**: `01001111 01100000` (in binary).
- **UTF-8 Encoding**: The character is encoded in 3 bytes:
  ```
  1110xxxx 10xxxxxx 10xxxxxx
  11100100 10111101 10100000
  ```
  - **Hexadecimal**: `E4 BD A0`
- **Memory Storage**: 3 bytes in memory: `E4 BD A0`.

| Character | Unicode Code Point | UTF-8 Encoding (Hex) | Memory Storage |
|-----------|--------------------|----------------------|----------------|
| 你         | 20320              | E4 BD A0             | 3 bytes        |

---

### **UTF-16 Encoding** (Fixed-Length for Basic Characters, Variable-Length for Others)
- **Definition**: UTF-16 uses **2 bytes** (16 bits) for most characters in the Basic Multilingual Plane (BMP, code points `0x0000` to `0xFFFF`). For characters outside the BMP (surrogate pairs), UTF-16 uses **4 bytes**.
- **How It Works**:
  - For characters in the BMP, it uses **2 bytes**.
  - For characters outside the BMP, it uses **4 bytes** in surrogate pairs.

**Example**: For `'你'` (code point `4F60`):
- **Binary for `4F60`**: `01001111 01100000` (in binary).
- **UTF-16 Encoding**: Directly encoded in 2 bytes:
  - **Hexadecimal**: `4F 60`
- **Memory Storage**: 2 bytes in memory: `4F 60`.

| Character | Unicode Code Point | UTF-16 Encoding (Hex) | Memory Storage |
|-----------|--------------------|----------------------|----------------|
| 你         | 20320              | 4F 60                | 2 bytes        |

---

### **UTF-32 Encoding** (Fixed-Length Encoding)
- **Definition**: UTF-32 uses **4 bytes** (32 bits) for every character, regardless of the code point.
- **How It Works**: UTF-32 stores characters in **4 bytes** (32 bits), which means every character, no matter how simple or complex, is always represented by 4 bytes.

**Example**: For `'你'` (code point `4F60`):
- **Binary for `4F60`**: `01001111 01100000` (in binary).
- **UTF-32 Encoding**: This is padded to 4 bytes:
  - **Hexadecimal**: `00 00 4F 60`
- **Memory Storage**: 4 bytes in memory: `00 00 4F 60`.

| Character | Unicode Code Point | UTF-32 Encoding (Hex) | Memory Storage |
|-----------|--------------------|----------------------|----------------|
| 你         | 20320              | 00 00 4F 60          | 4 bytes        |

---

### Comparison Table: ASCII, Unicode, and Encoding Types (UTF-8, UTF-16, UTF-32)

| Encoding | Description | Example Character | Unicode Code Point | Binary Representation | Hexadecimal | Bytes Used |
|----------|-------------|-------------------|---------------------|-----------------------|--------------|------------|
| **ASCII**  | 7-bit encoding for English characters | `A`                | `0x41` (65)           | `01000001`            | `0x41`       | 1 byte     |
| **UTF-8**  | Variable-length encoding (1 to 4 bytes) | `A`                | `0x41` (65)           | `01000001`            | `0x41`       | 1 byte     |
| **UTF-8**  | Variable-length encoding (1 to 4 bytes) | `你`                | `0x4F60` (20320)      | `11100100 10111101 10100000` | `E4 BD A0`   | 3 bytes    |
| **UTF-16** | Fixed-length for most characters (2 bytes) | `A`                | `0x41` (65)           | `00000000 01000001`   | `0x0041`     | 2 bytes    |
| **UTF-16** | Fixed-length for most characters (2 bytes) | `你`                | `0x4F60` (20320)      | `01001111 01100000`   | `0x4F60`     | 2 bytes    |
| **UTF-32** | Fixed-length encoding (4 bytes)         | `A`                | `0x41` (65)           | `00000000 00000000 00000000 01000001` | `00 00 00 41` | 4 bytes    |
| **UTF-32** | Fixed-length encoding (4 bytes)         | `你`                | `0x4F60` (20320)      | `00000000 00000000 01001111 01100000` | `00 00 4F 60` | 4 bytes    |

---

### How the Computer Stores These Characters in Memory:
- **In ASCII**: Each character is stored using 1 byte. For example, `'A'` is stored as `0x41`.
- **In UTF-8**: Characters like `'A'` are stored in 1 byte, but non-ASCII characters, like `'你'`, require 3 bytes (`E4 BD A0`).
- **In UTF-16**: Characters like `'A'` are stored using 2 bytes (`0041`), while `'你'` is stored using 2 bytes (`4F 60`).
- **In UTF-32**: Every character, including `'A'` and `'你'`, is stored using 4 bytes.

This system allows computers to store, transmit, and display text from any language in a standardized way, making it possible to handle global content efficiently.