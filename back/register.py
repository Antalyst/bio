import sys; sys.dont_write_bytecode = True # don't create __pycache__
import logging
from pyzkfp import ZKFP2
from time import sleep
from threading import Thread
import pymysql
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import asyncio
import threading
import base64
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Any, Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RegisterRequest(BaseModel):
    student_name: str
    age: int
    address: str
    examinee_no: str
    course_taken: str
    date_registered: str
    birthdate: str
class LoginRequest(BaseModel):
    username: str
    password: str

JWT_SECRET = "change_this_secret"
JWT_EXPIRE_MINUTES = 60

class AdminCreateRequest(BaseModel):
    username: str
    password: str



class FingerprintScanner:
    def verify_user_from_db(self, scanned_template):
        conn = None
        try:
            conn = pymysql.connect(**self.db_config, cursorclass=pymysql.cursors.DictCursor)
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM students")
                results = cursor.fetchall()
                if not results:
                    print('No users found in database.')
                    return False

                if str(type(scanned_template)) == "<class 'System.Byte[]>":
                    scanned_template = bytes(scanned_template)
                    print(f"Converted scanned_template to bytes, new length: {len(scanned_template)}")

                for result in results:
                    stored_template = result['fingerprint_template']
                    if str(type(stored_template)) == "<class 'System.Byte[]>":
                        stored_template = bytes(stored_template)

                    # Skip invalid data
                    if not stored_template or not scanned_template:
                        continue

                    match_score = self.zkfp2.DBMatch(stored_template, scanned_template)
                    if match_score > 200:
                        self.zkfp2.Light('green')
                        print(f"User verified with score {match_score}")
                        print(f"student_name: {result['student_name']}")
                        print(f"age: {result['age']}")
                        print(f"address: {result['address']}")
                        print(f"course_taken: {result['course_taken']}")
                        print(f"birthdate: {result['birthdate']}")
                        return {
                            "student_name": result['student_name'],
                            "age": result['age'],
                            "address": result['address'],
                            "course_taken": result['course_taken'],
                            "birthdate": result['birthdate']
                        }

                print("No matching fingerprint found.")
                self.zkfp2.Light('red', 1)
                return False
        except Exception as e:
            self.logger.error(f"Error verifying user: {e}")
            print(f"Error verifying user: {e}")
            return False
        finally:
            if conn:
                conn.close()

current_capture: Dict[str, Any] = {
    "status": "idle",
    "count": 0,
    "log": [],
    "fingerprint_template_b64": None,
    "student": None,
}
def __init__(self):
        self.logger = logging.getLogger('fps')
        fh = logging.FileHandler('logs.log')
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(fh)
        self.templates = []
        self.initialize_zkfp2()
        self.capture = None
        self.register = False
        self.fid = 1
        self.keep_alive = True
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'db': 'db',
            'charset': 'utf8mb4'
        }

def save_template_to_db(self, template_bytes,  student_data: RegisterRequest):
        if not isinstance(template_bytes, (bytes, bytearray)):
            print(f"Error: fingerprint template is not bytes, type: {type(template_bytes)}, value: {template_bytes}")
            self.logger.error(f"Fingerprint template is not bytes, type: {type(template_bytes)}, value: {template_bytes}")
            return
        conn = None
        try:
            conn = pymysql.connect(**self.db_config)
            with conn.cursor() as cursor:
                student_name = input('student_name: ')
                age = input('age: ')
                address = input('address: ')
                examinee_no = input('examinee_no: ')
                course_taken = input('course_taken: ')
                date_registered = input('date_registered: ')
                birthdate = input('birthdate: ')
                sql = """
                INSERT INTO students (student_name, age, address, examinee_no, course_taken, date_registered, birthdate, fingerprint_template)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (student_name, age, address, examinee_no, course_taken, date_registered, birthdate, template_bytes))
            conn.commit()
            self.logger.info('Fingerprint template saved to users table.')
        except Exception as e:
            self.logger.error(f'Error saving to DB: {e}')
        finally:
            if conn:
                conn.close()


@app.post("/verify-only")
def verify_only():
    try:
        zk = ZKFP2()
        zk.Init()
        zk.OpenDevice(0)
        zk.Light('green')
        print("Place your finger on the scanner...")
        while True:
            capture = zk.AcquireFingerprint()
            if not capture:
                sleep(0.1)
                continue
            tmp, img = capture
            print("Checking fingerprint in database (student table)...")
            conn = None
            try:
                conn = pymysql.connect(host='localhost', user='root', password='', db='db', cursorclass=pymysql.cursors.DictCursor)
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM student")
                    results = cursor.fetchall()
                    if not results:
                        zk.Light('red', 1)
                        raise HTTPException(status_code=404, detail="No records in database")
                    if str(type(tmp)) == "<class 'System.Byte[]'>":
                        tmp = bytes(tmp)
                    for row in results:
                        stored_template = row.get('fingerprint_template')
                        if str(type(stored_template)) == "<class 'System.Byte[]'>":
                            stored_template = bytes(stored_template)
                        if not stored_template or not tmp:
                            continue
                        score = zk.DBMatch(stored_template, tmp)
                        if score > 200:
                            zk.Light('green')
                            return {
                                "student_name": row.get('student_name'),
                                "age": row.get('age'),
                                "address": row.get('address'),
                                "course_taken": row.get('course_taken'),
                                "birthdate": row.get('birthdate'),
                            }
                    zk.Light('red', 1)
                    raise HTTPException(status_code=404, detail="No matching fingerprint found")
            finally:
                if conn:
                    conn.close()
    except HTTPException:
        raise
    except Exception as e:
        print(f"/verify-only error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    def initialize_zkfp2(self):
        self.zkfp2 = ZKFP2()
        self.zkfp2.Init()
        self.logger.info(f"{(i := self.zkfp2.GetDeviceCount())} Devices found. Connecting to the first device.")
        self.zkfp2.OpenDevice(0)
        self.zkfp2.Light("green")


    def capture_handler(self):
        try:
            tmp, img = self.capture
            if self.register:
                fid, score = self.zkfp2.DBIdentify(tmp)
                if fid:
                    self.logger.info(f"successfully identified the user: {fid}, Score: {score}")
                    self.zkfp2.Light('green')
                    self.capture = None
                    return
                if self.register:
                     if len(self.templates) < 3:
                        if not self.templates or self.zkfp2.DBMatch(self.templates[-1], tmp) > 0:
                            self.zkfp2.Light('green')
                            self.templates.append(tmp)
                            message = f"Finger {len(self.templates)} registered successfully! " + (f"{3-len(self.templates)} presses left." if 3-len(self.templates) > 0 else '')
                            self.logger.info(message)
                            if len(self.templates) == 3:
                                regTemp, regTempLen = self.zkfp2.DBMerge(*self.templates)
                                print(f"[DEBUG] regTemp type: {type(regTemp)}, length: {len(regTemp)}")
                                # Convert System.Byte[] to bytes if needed
                                if str(type(regTemp)) == "<class 'System.Byte[]'>":
                                    regTemp = bytes(regTemp)
                                    print(f"[DEBUG] regTemp converted to bytes, length: {len(regTemp)}")
                                self.save_template_to_db(regTemp)
                                self.templates.clear()
                                self.register = False
                                self.fid += 1

                            return message
                        else:
                            self.zkfp2.Light('red', 1)
                            self.logger.warning("Different finger. Please enter the original finger!")
            else:
                self.verify_user_from_db(tmp)
        except KeyboardInterrupt:
            self.logger.info("Shutting down...")
            self.zkfp2.Terminate()
            exit(0)
        self.capture = None


    def _capture_handler(self):
        try:
            self.capture_handler()
        except Exception as e:
            self.logger.error(e)
            self.capture = None


    def listenToFingerprints(self):
        try:
            while self.keep_alive:
                capture = self.zkfp2.AcquireFingerprint()
                if capture and not self.capture:
                    self.capture = capture
                    Thread(target=self._capture_handler, daemon=True).start()
                sleep(0.1)
        except KeyboardInterrupt:
            self.logger.info("Shutting down...")
            self.zkfp2.Terminate()
            exit(0)



@app.post("/register-user")
def register_user():
    fingerprint_scanner = FingerprintScanner()
    print("Place your finger on the scanner...")
    while True:
        capture = fingerprint_scanner.zkfp2.AcquireFingerprint()
        if capture:
            tmp, img = capture
            print("Checking fingerprint in database...")
            found = fingerprint_scanner.verify_user_from_db(tmp)
            if found:
                print("Fingerprint verified!");
                return found
            else:
                print("Fingerprint not found. Proceeding to registration.")
                try:
                    fingerprint_scanner.capture = capture
                    fingerprint_scanner.register = True
                    captureProgress = fingerprint_scanner.capture_handler()
                    return captureProgress
                except Exception as e:
                    print(f"Error during registration: {e}")
            sleep(1)


@app.post("/register-start")
def register_start():
    """Block until three successful taps are collected, then return merged template (base64)."""
    try:
        # initialize progress
        current_capture["status"] = "capturing"
        current_capture["count"] = 0
        current_capture["log"] = []
        current_capture["fingerprint_template_b64"] = None
        current_capture["student"] = None
        zk = ZKFP2()
        zk.Init()
        zk.OpenDevice(0)
        zk.Light('green')
        print("Place your finger on the scanner three times...")
        templates = []
        capture_log = []
        while True:
            capture = zk.AcquireFingerprint()
            if not capture:
                sleep(0.1)
                continue
            tmp, img = capture
            # Try early verification on first tap to avoid re-registering existing users
            if not templates:
                try:
                    conn = pymysql.connect(host='localhost', user='root', password='', db='db', cursorclass=pymysql.cursors.DictCursor)
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT * FROM student")
                        rows = cursor.fetchall()
                        check_tmp = bytes(tmp) if str(type(tmp)) == "<class 'System.Byte[]'>" else tmp
                        for row in rows:
                            stored = row.get('fingerprint_template')
                            if not stored:
                                continue
                            stored_b = bytes(stored) if str(type(stored)) == "<class 'System.Byte[]'>" else stored
                            score = zk.DBMatch(stored_b, check_tmp)
                            if score > 200:
                                zk.Light('green')
                                current_capture["status"] = "already_registered"
                                current_capture["student"] = {
                                    "student_name": row.get('student_name'),
                                    "age": row.get('age'),
                                    "address": row.get('address'),
                                    "course_taken": row.get('course_taken'),
                                    "birthdate": row.get('birthdate'),
                                }
                                current_capture["log"] = capture_log
                                return {"status": "already_registered", "message": "User already registered.", "student": {
                                    "student_name": row.get('student_name'),
                                    "age": row.get('age'),
                                    "address": row.get('address'),
                                    "course_taken": row.get('course_taken'),
                                    "birthdate": row.get('birthdate'),
                                }}
                except Exception as _:
                    pass
                finally:
                    try:
                        if conn:
                            conn.close()
                    except Exception:
                        pass
            if not templates:
                templates.append(tmp)
                zk.Light('green')
                print("Finger 1 registered successfully! 2 presses left.")
                capture_log.append("Finger 1 registered successfully! 2 presses left.")
                current_capture["count"] = len(templates)
                current_capture["log"] = capture_log[:]
                sleep(0.3)
                continue
            last_template = templates[-1]
            if zk.DBMatch(last_template, tmp) > 0:
                templates.append(tmp)
                remaining = 3 - len(templates)
                zk.Light('green')
                if remaining > 0:
                    print(f"Finger {len(templates)} registered successfully! {remaining} presses left.")
                    capture_log.append(f"Finger {len(templates)} registered successfully! {remaining} presses left.")
                current_capture["count"] = len(templates)
                current_capture["log"] = capture_log[:]
                sleep(0.3)
            else:
                zk.Light('red', 1)
                print("Different finger. Please enter the original finger!")
                capture_log.append("Different finger. Please enter the original finger!")
                current_capture["log"] = capture_log[:]
                sleep(0.3)

            if len(templates) == 3:
                regTemp, regTempLen = zk.DBMerge(*templates)
                if str(type(regTemp)) == "<class 'System.Byte[]'>":
                    regTemp = bytes(regTemp)
                template_b64 = base64.b64encode(regTemp).decode('utf-8')
                current_capture["status"] = "done"
                current_capture["fingerprint_template_b64"] = template_b64
                current_capture["count"] = 3
                current_capture["log"] = capture_log[:]
                return {"status": "ok", "message": "Fingerprint captured.", "fingerprint_template_b64": template_b64, "capture_log": capture_log}
    except Exception as e:
        print(f"Error during capture: {e}")
        current_capture["status"] = "error"
        raise HTTPException(status_code=500, detail="Failed to capture fingerprint.")


@app.get("/register-progress")
def register_progress():
    # Return a shallow copy to avoid accidental mutation by clients
    return {
        "status": current_capture.get("status"),
        "count": current_capture.get("count", 0),
        "log": current_capture.get("log", []),
        "fingerprint_template_b64": current_capture.get("fingerprint_template_b64"),
        "student": current_capture.get("student"),
    }


class SaveStudentRequest(RegisterRequest):
    fingerprint_template_b64: str


@app.post("/register-save")
def register_save(payload: SaveStudentRequest):
    try:
        template_bytes = base64.b64decode(payload.fingerprint_template_b64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid fingerprint_template_b64")

    conn = None
    try:
        conn = pymysql.connect(host='localhost', user='root', password='', db='db', charset='utf8mb4')
        with conn.cursor() as cursor:
            sql = (
                "INSERT INTO student (student_name, age, address, examinee_no, course_taken, date_registered, birthdate, fingerprint_template) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(
                sql,
                (
                    payload.student_name,
                    payload.age,
                    payload.address,
                    payload.examinee_no,
                    payload.course_taken,
                    payload.date_registered,
                    payload.birthdate,
                    pymysql.Binary(template_bytes),
                ),
            )
        conn.commit()
        return {"status": "ok", "message": "Student registered successfully."}
    except Exception as e:
        print(f"/register-save error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@app.post("/verify-user")
def register_user():
    fingerprint_scanner = FingerprintScanner()
    print("Place your finger on the scanner...")
    while True:
        capture = fingerprint_scanner.zkfp2.AcquireFingerprint()
        if capture:
            tmp, img = capture
            print("Checking fingerprint in database...")
            found = fingerprint_scanner.verify_user_from_db(tmp)
            if found:
                print("Fingerprint verified!");
                return found
            else:
                print("Fingerprint not found. Proceeding to registration.")
                try:
                    fingerprint_scanner.capture = capture
                    fingerprint_scanner.register = True
                    captureProgress = fingerprint_scanner.capture_handler()
                    return captureProgress
                except Exception as e:
                    print(f"Error during registration: {e}")
            sleep(1)



@app.post("/admin-create")
def admin_create(payload: AdminCreateRequest):
    if not payload.username or not payload.password:
        raise HTTPException(status_code=400, detail="username and password are required")
    conn = None
    try:
        conn = pymysql.connect(host='localhost', user='root', password='', db='db', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        with conn.cursor() as cursor:
            # check if exists
            cursor.execute("SELECT id FROM admin WHERE username=%s", (payload.username,))
            if cursor.fetchone():
                raise HTTPException(status_code=409, detail="username already exists")
            hashed = bcrypt.hashpw(payload.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute("INSERT INTO admin (username, password) VALUES (%s, %s)", (payload.username, hashed))
        conn.commit()
        return {"status": "ok", "message": "admin created"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@app.post("/login")
def login(payload: LoginRequest):
    conn = None
    try:
        conn = pymysql.connect(host='localhost', user='root', password='', db='db', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM admin WHERE username=%s", (payload.username,))
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            stored_hash = row['password']
            if not bcrypt.checkpw(payload.password.encode('utf-8'), stored_hash.encode('utf-8')):
                raise HTTPException(status_code=401, detail="Invalid credentials")
            exp = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
            token = jwt.encode({"sub": payload.username, "exp": exp}, JWT_SECRET, algorithm="HS256")
            return {"token": token}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("register:app", port=8000, reload=True)