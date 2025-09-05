Farm Management Dashboard  

A Tkinter-based desktop application for managing livestock records and vaccination schedules.  
This app provides an easy-to-use dashboard where you can track animals, health information, and farm-related data.  

---

Features  

- 📋Livestock Inventory Management
  - Add, view, and organize animal records.  
  - Store details such as Tag ID, Species, Breed, Age, Weight, Health, and Location.  

- 💉 Vaccination Tracking  
  - Record last vaccination date and next required vaccination date.  
  - Get automatic warnings when vaccination dates are overdue.  
  - Overdue animals are highlighted in **red** in the table.  

- 💾 Persistent Storage
  - Data is saved in a `livestock_data.json` file.  
  - Automatically loads and updates records across sessions.  

- 🎨 User-Friendly Interface 
  - Built with Tkinter & ttk widgets.  
  - Alternating row colors for readability.  
  - Clean, modern look with bold headers and intuitive controls.  

---

## 📂 Project Structure  

```
farm_dashboard/
│── main.py                  # Main entry point of the app
│── sidebar.py               # Sidebar navigation system
│── profile.py               # User profile page
│── livestock_inventory.py   # Livestock management module
│── livestock_data.json      # Data storage file (auto-created)
│── README.md                # Project documentation
```

---

## 🚀 Getting Started  

### 1. Clone the Repository  
```bash
git clone https://github.com/your-username/farm-dashboard.git
cd farm-dashboard
```

### 2. Run the App  
This project uses only Python’s standard libraries (`tkinter`, `json`, `os`, `datetime`).  
No extra dependencies required ✅  

```bash
python main.py
```

---

## 📖 Example JSON Structure  

The `livestock_data.json` file is automatically created and updated. Example:  

```json
{
  "livestock": [
    {
      "id": "COW123",
      "type": "Cow",
      "breed": "Friesian",
      "age": 4,
      "weight": 450.5,
      "health": "Good",
      "location": "Barn A",
      "last_vaccination": "2025-08-01",
      "next_vaccination": "2025-09-01"
    }
  ]
}
```

---

## 🔮 Future Improvements  

- ✏️ Edit & delete animal records  
- 📊 Farm statistics dashboard (charts for herd size, vaccination status, etc.)  
- 📤 Export/import records as CSV/Excel  
- 🌐 Cloud storage & multi-user support  

---

## 👨‍💻 Author  

Developed by Bajeh Abel Ojochide 
📧 Contact: [chidejohn63@gmail.com] 
🔗 GitHub: [github.com/abelbajeh]  
