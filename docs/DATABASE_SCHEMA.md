# 🗄️ Database & JSON Store Schema Reference

This document outlines the entity relationships, JSON datastores, and field definitions across the **Student Resource Sharing Platform**.

---

## 1. Entity Relationship Overview

```text
[User Profile] (users.json)
       │ 1
       │ has many
       ▼ N
[Study Material Meta] (materials_meta.json) ── has many ──► [Peer Reviews & Ratings]
       │
       │ has
       ▼
[PDF Storage File] (materials/*.pdf)

[User Profile]
       │ 1
       │ has
       ▼ N
[Attendance Tracking] (attendance.json)
```

---

## 2. Store Definitions

### `users.json`
| Field | Type | Description |
|---|---|---|
| `key (username)` | string | Unique student or faculty handle |
| `name` | string | Full display name |
| `password` | string | SHA-256 password digest |
| `branch` | string | Academic discipline/department |
| `semester` | string | Current semester |
| `role` | string | `Student` or `Admin` / `Faculty` |
| `karma` | integer | Academic reputation points |
| `badges` | list | List of unlocked achievement badge keys |

### `materials_meta.json`
| Field | Type | Description |
|---|---|---|
| `key (filename)` | string | PDF file basename inside `materials/` |
| `title` | string | Academic title of study document |
| `subject` | string | Course name |
| `topic` | string | Unit / topic covered |
| `uploaded_by` | string | Username of contributor |
| `status` | string | `Approved`, `Pending`, or `Rejected` |
| `rating` | float | Average student star rating (1.0 - 5.0) |
| `downloads` | integer | Total download count |
| `timestamp` | string | ISO format upload timestamp |

---

## 3. Data Integrity Constraints
1. **Atomic File Writes**: Metadata updates use atomic tempfile swap to prevent JSON corruption during concurrent operations.
2. **Key Uniqueness**: Usernames and PDF filenames serve as primary unique keys.
