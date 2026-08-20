import os
import json
from datetime import datetime

class PDFDocument:
    def __init__(self, title, subject, semester, doc_type, author="Faculty / Subject Lead"):
        self.title = title
        self.subject = subject
        self.semester = semester
        self.doc_type = doc_type
        self.author = author
        self.pages = []
        self.current_page = []
        self.page_num = 0
        self.new_page()

    def new_page(self):
        if self.current_page:
            self.pages.append("\n".join(self.current_page))
        self.current_page = []
        self.page_num += 1
        self.draw_page_decorations()

    def draw_page_decorations(self):
        # Header banner
        self.current_page.append("0.2 0.28 0.65 rg") # Blue-Indigo
        self.current_page.append("35 745 542 35 re f")
        
        # Header text
        self.current_page.append("BT /F1 11 Tf 1 1 1 rg 45 758 Td (CampusHub Study Hub | " + self.escape(self.subject) + ") Tj ET")
        self.current_page.append("BT /F2 9 Tf 0.85 0.9 1 rg 460 758 Td (" + self.escape(self.semester) + ") Tj ET")
        
        # Footer
        self.current_page.append("0.75 0.8 0.9 RG 1 w")
        self.current_page.append("35 40 m 577 40 l S")
        self.current_page.append("BT /F2 8 Tf 0.4 0.45 0.55 rg 45 28 Td (CampusHub Academic Notes - Certified Peer Resource) Tj ET")
        self.current_page.append(f"BT /F2 8 Tf 0.4 0.45 0.55 rg 530 28 Td (Page {self.page_num}) Tj ET")

    def escape(self, text):
        return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    def add_title_block(self, main_title, subtitle):
        self.current_page.append("0.94 0.96 0.99 rg 35 660 542 70 re f")
        self.current_page.append("0.25 0.35 0.75 RG 1.5 w 35 660 542 70 re S")
        self.current_page.append("BT /F1 15 Tf 0.1 0.15 0.4 rg 48 705 Td (" + self.escape(main_title) + ") Tj ET")
        self.current_page.append("BT /F2 10 Tf 0.25 0.3 0.45 rg 48 688 Td (" + self.escape(subtitle) + ") Tj ET")
        self.current_page.append("BT /F2 8.5 Tf 0.4 0.45 0.55 rg 48 672 Td (Author: " + self.escape(self.author) + " | Type: " + self.escape(self.doc_type) + " | Verified 2026) Tj ET")

    def add_section_heading(self, y_pos, title):
        self.current_page.append("0.88 0.92 0.98 rg")
        self.current_page.append(f"35 {y_pos-4} 542 20 re f")
        self.current_page.append("0.2 0.3 0.7 rg")
        self.current_page.append(f"35 {y_pos-4} 4 20 re f")
        self.current_page.append(f"BT /F1 10.5 Tf 0.12 0.18 0.45 rg 46 {y_pos+1} Td (" + self.escape(title) + ") Tj ET")

    def add_text_lines(self, y_start, lines, font_size=9, line_height=12.5):
        y = y_start
        for line in lines:
            if line.startswith("•") or line.startswith("-"):
                self.current_page.append(f"BT /F2 {font_size} Tf 0.15 0.15 0.2 rg 48 {y} Td (" + self.escape(line) + ") Tj ET")
            elif line.startswith(">>") or line.startswith("💡"):
                self.current_page.append(f"BT /F1 {font_size} Tf 0.1 0.35 0.2 rg 48 {y} Td (" + self.escape(line) + ") Tj ET")
            else:
                self.current_page.append(f"BT /F2 {font_size} Tf 0.15 0.15 0.2 rg 38 {y} Td (" + self.escape(line) + ") Tj ET")
            y -= line_height
        return y

    def add_code_box(self, y_top, height, code_lines):
        self.current_page.append(f"0.12 0.15 0.22 rg 38 {y_top-height} 536 {height} re f")
        self.current_page.append(f"0.3 0.4 0.65 RG 1 w 38 {y_top-height} 536 {height} re S")
        y = y_top - 12
        for line in code_lines:
            self.current_page.append(f"BT /F3 8.5 Tf 0.4 0.9 0.5 rg 48 {y} Td (" + self.escape(line) + ") Tj ET")
            y -= 11
        return y_top - height - 10

    def compile(self, output_filepath):
        if self.current_page:
            self.pages.append("\n".join(self.current_page))

        objects = []
        objects.append("<< /Type /Catalog /Pages 2 0 R >>")
        
        kids = " ".join([f"{3 + i*2} 0 R" for i in range(len(self.pages))])
        objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(self.pages)} >>")

        font_res = "<< /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >> /F2 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> /F3 << /Type /Font /Subtype /Type1 /BaseFont /Courier >> >>"

        obj_num = 3
        for page_stream in self.pages:
            content_len = len(page_stream.encode("utf-8"))
            page_obj = f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font {font_res} >> /Contents {obj_num+1} 0 R >>"
            stream_obj = f"<< /Length {content_len} >>\nstream\n{page_stream}\nendstream"
            objects.append(page_obj)
            objects.append(stream_obj)
            obj_num += 2

        with open(output_filepath, "wb") as f:
            f.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
            offsets = []
            for i, obj in enumerate(objects):
                offsets.append(f.tell())
                f.write(f"{i+1} 0 obj\n{obj}\nendobj\n".encode("utf-8"))

            xref_offset = f.tell()
            f.write(f"xref\n0 {len(objects)+1}\n".encode("utf-8"))
            f.write(b"0000000000 65535 f \n")
            for offset in offsets:
                f.write(f"{offset:010d} 00000 n \n".encode("utf-8"))

            f.write(f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("utf-8"))


# ----------------------------------------------------
# 1. C PROGRAMMING PDF
# ----------------------------------------------------
def generate_c_pdf():
    pdf = PDFDocument(
        title="C Programming Complete Reference & Notes",
        subject="C Programming",
        semester="1st Semester",
        doc_type="Lecture Notes",
        author="Prof. K. Sharma (CS Dept)"
    )
    pdf.add_title_block("C Programming Master Guide", "Comprehensive Reference: Syntax, Pointers, Memory Management & Structs")
    y = 640
    pdf.add_section_heading(y, "1. Core Syntax & Data Types")
    y = pdf.add_text_lines(y - 14, [
        "• C is a statically typed, procedural programming language developed by Dennis Ritchie.",
        "• Fundamental Types: char (1B), int (4B), float (4B), double (8B), void (empty).",
        "• Standard I/O functions: printf() for formatted output, scanf() for reading user input."
    ])
    y -= 4
    pdf.add_section_heading(y, "2. Structure of a Standard C Program")
    y = pdf.add_code_box(y - 8, 70, [
        "#include <stdio.h>",
        "int main() {",
        "    int a = 10, b = 20;",
        "    printf(\"Sum: %d\\n\", a + b);",
        "    return 0;",
        "}"
    ])
    y -= 4
    pdf.add_section_heading(y, "3. Pointers & Dynamic Memory (stdlib.h)")
    y = pdf.add_text_lines(y - 14, [
        "• Pointer syntax: int *ptr = &val; (* is dereference, & is address-of).",
        "• malloc(size): Allocates raw memory on heap; free(ptr) deallocates memory."
    ])
    pdf.compile("materials/C_Programming_Complete_Notes.pdf")


# ----------------------------------------------------
# 2. C++ PROGRAMMING (OOPs & STL) PDF
# ----------------------------------------------------
def generate_cpp_pdf():
    pdf = PDFDocument(
        title="C++ Object-Oriented Programming & STL Master Guide",
        subject="C++ Programming",
        semester="2nd Semester",
        doc_type="Lecture Notes",
        author="Prof. R. Verma (Computer Science)"
    )
    pdf.add_title_block("C++ OOPs & Standard Template Library", "Four Pillars of OOP, Virtual Functions, Templates, Vector, Map & Algorithms")
    y = 640
    pdf.add_section_heading(y, "1. The Four Pillars of OOP in C++")
    y = pdf.add_text_lines(y - 14, [
        "• Encapsulation: Bundling data and methods inside classes with private/public access.",
        "• Abstraction: Hiding internal details using pure virtual functions.",
        "• Inheritance: Deriving child classes from base classes.",
        "• Polymorphism: Function overloading (compile-time) and virtual methods (runtime)."
    ])
    y -= 4
    pdf.add_section_heading(y, "2. Standard Template Library (STL)")
    y = pdf.add_code_box(y - 8, 75, [
        "#include <vector>",
        "#include <algorithm>",
        "vector<int> v = {4, 1, 8, 3};",
        "sort(v.begin(), v.end()); // O(n log n)",
        "v.push_back(10);"
    ])
    pdf.compile("materials/CPP_OOPs_and_STL_Guide.pdf")


# ----------------------------------------------------
# 3. PYTHON PROGRAMMING PDF
# ----------------------------------------------------
def generate_python_pdf():
    pdf = PDFDocument(
        title="Python Complete Programming Handbook",
        subject="Python",
        semester="1st Semester",
        doc_type="Lecture Notes",
        author="Dr. S. Mehta (AI & Data Science Lead)"
    )
    pdf.add_title_block("Python Complete Programming Handbook", "Core Data Structures, OOP, Exception Handling, File I/O & NumPy Basics")
    y = 640
    pdf.add_section_heading(y, "1. Core Python Collections & Comprehensions")
    y = pdf.add_text_lines(y - 14, [
        "• Lists (mutable), Tuples (immutable), Dictionaries (O(1) hash maps), Sets (unique).",
        "• List comprehension: evens = [x for x in range(20) if x % 2 == 0]"
    ])
    y -= 4
    pdf.add_section_heading(y, "2. OOP & Dunder Methods")
    y = pdf.add_code_box(y - 8, 75, [
        "class Student:",
        "    def __init__(self, name, gpa):",
        "        self.name = name",
        "        self.gpa = gpa",
        "    def __str__(self):",
        "        return f\"{self.name} ({self.gpa})\""
    ])
    pdf.compile("materials/Python_Complete_Programming_Handbook.pdf")


# ----------------------------------------------------
# 4. DSA QUICK REVISION CHEATSHEET PDF
# ----------------------------------------------------
def generate_dsa_quick_revision_pdf():
    pdf = PDFDocument(
        title="DSA & Algorithms 1-Page Quick Revision Cheatsheet",
        subject="Data Structures",
        semester="3rd Semester",
        doc_type="Quick Revision Cheatsheet",
        author="Tech Society Editorial Board"
    )
    pdf.add_title_block("DSA & Algorithms Rapid Revision Card", "Master Big-O Complexities, Sorting Comparison, Trees, Graphs & DP Patterns")
    
    y = 640
    pdf.add_section_heading(y, "1. Sorting Algorithms Complexity Master Matrix")
    y = pdf.add_text_lines(y - 14, [
        "• QuickSort: Best O(n log n) | Avg O(n log n) | Worst O(n^2) | Space O(log n)",
        "• MergeSort: Best O(n log n) | Avg O(n log n) | Worst O(n log n) | Space O(n) [Stable]",
        "• HeapSort: Best O(n log n) | Avg O(n log n) | Worst O(n log n) | Space O(1) [In-place]",
        "• InsertionSort: Best O(n) | Avg O(n^2) | Worst O(n^2) | Space O(1) [Great for small/almost sorted]"
    ])
    
    y -= 4
    pdf.add_section_heading(y, "2. Trees, Graphs & Shortest Path Formulae")
    y = pdf.add_text_lines(y - 14, [
        "• Balanced BST Search/Insert/Delete: O(log n) time.",
        "• BFS (Breadth-First Search): Queue-based, shortest path in unweighted graphs, O(V + E).",
        "• DFS (Depth-First Search): Stack/Recursion, cycle detection & topological sort, O(V + E).",
        "• Dijkstra's Algorithm: Min-Heap / Priority Queue, O((V + E) log V) with non-negative weights."
    ])
    
    y -= 4
    pdf.add_section_heading(y, "3. Dynamic Programming 14-Pattern Quick Map")
    y = pdf.add_text_lines(y - 14, [
        "• 0/1 Knapsack: dp[i][w] = max(dp[i-1][w], val[i] + dp[i-1][w-wt[i]])",
        "• Longest Common Subsequence (LCS): if s1[i]==s2[j] -> 1 + dp[i-1][j-1] else max(dp[i-1][j], dp[i][j-1])"
    ])

    pdf.compile("materials/DSA_and_Core_CS_Quick_Revision_Cheatsheet.pdf")


# ----------------------------------------------------
# 5. OS & DBMS EXAM CHEATSHEET PDF
# ----------------------------------------------------
def generate_os_dbms_cheatsheet_pdf():
    pdf = PDFDocument(
        title="OS & DBMS Core Concepts Exam Revision Sheet",
        subject="Operating Systems",
        semester="4th Semester",
        doc_type="Quick Revision Cheatsheet",
        author="Campus Exam Prep Lead"
    )
    pdf.add_title_block("OS & DBMS Rapid Exam Revision Guide", "CPU Scheduling, Deadlocks, Paging, ACID Properties & Normalization")
    
    y = 640
    pdf.add_section_heading(y, "1. Operating Systems High-Yield Concepts")
    y = pdf.add_text_lines(y - 14, [
        "• 4 Conditions for Deadlock: Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait.",
        "• Banker's Algorithm: Need[i][j] = Max[i][j] - Allocation[i][j]. Check if Safe State exists.",
        "• Page Replacement: FIFO (Belady's Anomaly), LRU (Optimal practical), Optimal (Lowest page faults)."
    ])
    
    y -= 4
    pdf.add_section_heading(y, "2. DBMS & SQL Core Formulae")
    y = pdf.add_text_lines(y - 14, [
        "• ACID: Atomicity (All or None), Consistency (Rules valid), Isolation (Concurrency safe), Durability (Committed persists).",
        "• 1NF: Atomic values; 2NF: 1NF + No partial dependency; 3NF: 2NF + No transitive dependency.",
        "• BCNF (Boyce-Codd): For every X -> Y, X must be a super key."
    ])

    pdf.compile("materials/OS_and_DBMS_Exam_CheatSheet.pdf")


if __name__ == "__main__":
    os.makedirs("materials", exist_ok=True)
    generate_c_pdf()
    generate_cpp_pdf()
    generate_python_pdf()
    generate_dsa_quick_revision_pdf()
    generate_os_dbms_cheatsheet_pdf()
    print("All Programming & Quick Revision PDFs generated successfully in materials/!")
