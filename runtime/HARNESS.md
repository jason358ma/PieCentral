# Design Goals for Runtime Test Harness
- Emulate Dawn (at least as far as uploading/downloading)
- Allow for multiple test code files (allows testing invalid syntax, other oddities)
- (Maybe) Integrate with virtual sensors to fully test integration

## What Should We Test?
- A wide variety of plausible failure cases: missing API arguments, incorrect types, incorrect arguments
- A typical student code file
- Code uploading and downloading