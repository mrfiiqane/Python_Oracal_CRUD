import oracledb
import os

# Database Connection Details
DB_USER = "STUDENT MANAGEMENT CRUD"
DB_PASSWORD = "123"
DB_DSN = "192.168.249.121:4500/XE" || "http://127.0.0.1:8080/apex/f?p=4500:1003:4242725812613691::NO:::" # Explicitly including port 1521

try:
    # Enable Thick Mode for older Oracle versions (like 11g)
    oracledb.init_oracle_client()
except Exception as e:
    print(f"Note: Thick mode initialization skipped or failed: {e}")

def get_db_connection():
    try:
        conn = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )
        return conn, None
    except Exception as e:
        error_msg = str(e)
        print(f"Error connecting to Oracle DB: {error_msg}")
        return None, error_msg

def init_db():
    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Check if STUDENTS table exists in the CURRENT schema
            cursor.execute("""
                SELECT COUNT(*) FROM user_tables WHERE table_name = 'STUDENTS'
            """)
            if cursor.fetchone()[0] == 0:
                print("Setting up Oracle 11g compatible table...")
                
                # 1. Create Table (11g compatible)
                cursor.execute("""
                    CREATE TABLE STUDENTS (
                        ID NUMBER PRIMARY KEY,
                        NAME VARCHAR2(100) NOT NULL,
                        EMAIL VARCHAR2(100) NOT NULL,
                        COURSE VARCHAR2(100),
                        CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # 2. Create Sequence for ID
                cursor.execute("CREATE SEQUENCE students_seq START WITH 1")
                
                # 3. Create Trigger for Auto-Increment
                cursor.execute("""
                    CREATE OR REPLACE TRIGGER students_bir
                    BEFORE INSERT ON STUDENTS
                    FOR EACH ROW
                    BEGIN
                      IF :new.id IS NULL THEN
                        SELECT students_seq.NEXTVAL INTO :new.id FROM dual;
                      END IF;
                    END;
                """)
                
                conn.commit()
                print("Database initialized successfully with 11g Sequence/Trigger.")
            else:
                print("Table 'STUDENTS' already exists.")
        except Exception as e:
            print(f"Error initializing 11g database: {e}")
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    init_db()
