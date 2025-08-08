<p align="center">
    <img src="https://cdn.discordapp.com/attachments/783810268760768552/1403171315657080882/IMG_20250808_021927.jpg?ex=6896949f&is=6895431f&hm=d5b5c1315e088d8b2ccd6a19cb3d6e51325424a60e3a2f6887645ddbc0252226" width="180" alt="GitInfo Logo">
</p>

<table align="center">
  <tr>
    <td align="center">
      <a href="https://opensource.org/licenses/apache-2-0"><img src="https://img.shields.io/badge/License-Apache-green.svg" alt="License: Apache License 2.0"></a>
    </td>
    <td align="center">
      <img src="https://img.shields.io/badge/Build-Passing-green" alt="Build Passing">
    </td>
    <td align="center">
      <img src="https://img.shields.io/badge/Version-v0.1.0-blue" alt="Version">
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://img.shields.io/badge/Author-rompelhd-red" alt="Author: rompelhd">
    </td>
    <td align="center">
      <img src="https://img.shields.io/badge/Platform-All%20Linux%20%7C%20macOS%20%7C%20Windows-yellowgreen?style=flat&labelColor=gray" alt="Platform">
    </td>
    <td align="center">
      <img src="https://img.shields.io/badge/Python-3.x-orange" alt="Python Version">
    </td>
  </tr>
</table>

<br/>

**GitInfo** is a lightweight tool for analyzing Git repositories, offering an efficient way to count lines of code and gather repository statistics. It's a simple yet powerful tool for developers and teams.

---

## Features

- 🧮 **Count Lines of Code**  
  Measure the total number of lines in supported programming files in the repository.

- 📂 **Language Support**  
  Analyze repositories with files in Python, JavaScript, C++, Java, HTML, CSS, Markdown, and more.

- ⚡ **Fast Processing**  
  Utilizes multi-threaded file parsing for optimized performance.

- 🌐 **Planned Features**  
  Future updates will include integration with GitHub to fetch stars, forks, and followers.

---

## Installation

To install **GitInfo**, clone the repository and install dependencies:

```bash
git clone https://github.com/rompelhd/GitInfo.git
cd GitInfo
pip install -r requirements.txt
```

---

## Usage

Run **GitInfo** by providing the repository URL:

```bash
python GitInfo.py <repository_url>
```

### Example

```bash
python GitInfo.py https://github.com/torvalds/linux
```

### Output

- **Lines of Code**: Total lines across supported files.  
- **Repository Details**: Owner, name, and other metadata.

---

## Supported File Extensions

`.py`, `.js`, `.java`, `.c`, `.cpp`, `.html`, `.css`, `.md`, and others.

---

## Roadmap

- **GitHub API Integration**  
  Retrieve repository stars, forks, and followers.  

- **Custom Extensions**  
  Allow users to specify additional or excluded file types.  

- **Enhanced Reporting**  
  Generate charts and statistics with detailed insights.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.  
2. Create a branch for your feature or bugfix.  
3. Submit a pull request for review.  

---

## License

This project is licensed under the [Apache License](https://opensource.org/licenses/apache-2-0).

---
