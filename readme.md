# 🎓 Student Resource Sharing Platform

A modern, interactive web application built with **Streamlit** to help college students easily upload, search, download study materials, explore learning resources, and view college announcements.

---

## 📋 Table of Contents

1. [System Overview](#-system-overview)
2. [Architecture & Component Diagram](#-architecture--component-diagram)
3. [Component Breakdown](#-component-breakdown)
4. [Comprehensive System Audit](#-comprehensive-system-audit)
   - [Summary Scorecard](#summary-scorecard)
   - [Critical & High Severity Findings](#1-critical--high-severity-findings)
   - [Medium Severity Findings](#2-medium-severity-findings)
   - [Low Severity & Code Quality Findings](#3-low-severity--code-quality-findings)
5. [Remediation & Improvement Roadmap](#-remediation--improvement-roadmap)
6. [Getting Started & Local Setup](#-getting-started--local-setup)
7. [License](#-license)

---

## 🌟 System Overview

The **Student Resource Sharing Platform** is designed to streamline academic collaboration among college students. The system allows students to:
- Browse and download course-specific PDF study materials.
- Upload new academic resources for peer access.
- Check campus and department announcements.
- Access curated references for coding and technical interview prep.
- Run auxiliary terminal tools (Hangman Word Guessing Game & Multi-function Calculator).

---

## 🛠️ Tech Stack

- **Frontend & Backend Framework**: [Streamlit](https://streamlit.io/)
- **Programming Language**: Python 3.x
- **Storage**: Local filesystem storage (`materials/` folder for PDF files)

---

## 📁 Project Structure

```text
.
├── app.py               # Main Streamlit application
├── materials/           # Storage directory for uploaded PDF study materials
├── announcements.json   # College announcements data
├── project1.py          # Terminal-based fruit word guessing game
├── test/
│   └── calculator.py    # Console calculator script
├── .gitignore           # Git ignore file
└── README.md            # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

Ensure you have **Python 3.8+** installed on your system.

### 1. Installation

Clone this repository or download the project files, then install the required dependencies:

```bash
pip install streamlit
```

### 2. Running the Application

Launch the Streamlit app by running:

```bash
streamlit run app.py
```

The web application will automatically open in your default browser at `http://localhost:8501`.

---

## 📝 License

This project is open-source and available for educational and student use.
