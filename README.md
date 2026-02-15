# Smart Attendance System: AI Face Recognition with Cloud Integration

An automated, real-time attendance management system that leverages Computer Vision to identify individuals and synchronizes data to the cloud. By replacing manual roll calls with facial recognition and **Firebase** integration, this system provides a scalable, paperless solution for tracking attendance in real-time.

## 🚀 Key Features

* **Real-time Face Detection:** Uses OpenCV to detect and track faces in a live video stream with low-latency performance.
* **High-Accuracy Recognition:** Utilizes 128-d facial embeddings and deep learning to identify individuals against a registered database.
* **Firebase Cloud Integration:**
    * **Realtime Database:** Attendance logs (Name, Timestamp, Date) are synced instantly to the cloud.
    * **Cloud Storage:** Stores and retrieves user profile images for centralized management.
* **Automated Duplicate Prevention:** Logic-driven system that ensures a user is marked "Present" only once per session, preventing redundant entries.
* **Scalable Architecture:** Designed to support multiple entry points syncing to a single cloud dashboard.

## 🛠️ Tech Stack

* **Languages:** Python
* **Computer Vision:** OpenCV (`cv2`), `face_recognition` (dlib-based)
* **Cloud Infrastructure:** **Firebase (Realtime Database & Cloud Storage)**
* **Database Management:** Firebase Admin SDK, JSON, Pandas
* **Tools:** NumPy, Pickle (for local embedding storage)

## 📁 Project Structure

* `main.py`: The primary engine that handles the camera feed, face recognition, and Firebase data push.
* `capture_image.py`: Module for registering new users and uploading their profile photos to Firebase Storage.
* `firebase_config.py`: Handles the connection and authentication with the Firebase Service Account.
* `encodings.pickle`: Local cache of facial embeddings to ensure rapid offline/online matching.

## 📊 Methodology

1.  **Identity Verification:** The system captures a frame, detects a face, and generates a unique encoding.
2.  **Matching:** The encoding is compared against the known database. If a match is found, the system verifies the identity.
3.  **Firebase Sync:**
    * The system checks the **Firebase Realtime Database** to see if the user has already checked in.
    * If not, it pushes a new record with a precise `ISO 8601` timestamp.
4.  **Admin View:** Data is immediately visible in the Firebase Console or any connected web/mobile dashboard.

## 📈 Impact

* **Efficiency:** Reduced manual attendance time by ~90%.
* **Accuracy:** Eliminated "proxy" attendance through unique biometric verification.
* **Accessibility:** Attendance records are accessible globally via the Firebase cloud console.

---

### ⚙️ Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/lazm27/Attendance-System.git](https://github.com/lazm27/Attendance-System.git)
    ```

2.  **Install Dependencies:**
    ```bash
    pip install opencv-python face_recognition firebase-admin pandas
    ```

3.  **Firebase Setup:**
    * Create a project in the [Firebase Console](https://console.firebase.google.com/).
    * Download your `serviceAccountKey.json` and place it in the root directory.
    * Update the `databaseURL` and `storageBucket` in your config script.

4.  **Run the System:**
    ```bash
    python main.py
    ```
