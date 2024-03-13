import sqlite3


class Server:
    """Server"""
    def __init__(self):
        con = sqlite3.connect("labels.db")
        self.cur = con.cursor()
        self.create_label_table()

    def create_label_table(self):
        """Create label table."""
        self.cur.execute("""CREATE TABLE IF NOT EXISTS labels (
            label_id TEXT PRIMARY KEY,
            label TEXT NOT NULL,
            prompt TEXT,
            response TEXT
        )""")

    def insert_label(self, label_id: str, label: str, prompt_response: dict) -> None:
        """Insert a label into the database."""
        query = (
            f"INSERT INTO labels VALUES ({label_id}, '{label}',"
            f" '{prompt_response['prompt']}', '{prompt_response['response']}')"
            )
        try:
            self.cur.execute(
                query
            )
        except sqlite3.OperationalError: ## temporary error handling fix to logging later
            print("Error in inserting new label: "+query+"\n")
    
    def get_label_list(self):
        """Get dict of label_id:labels in the database."""
        self.cur.execute("SELECT label_id,label FROM labels ORDER BY label ASC;")
        # return as a list of dict of label_id: label
        rows = self.cur.fetchall()
        label_dict = {row[0]: row[1] for row in rows}
        return label_dict

    def get_prompt_responses(self, label_ids: list) -> dict:
        """Get prompt responses from the database."""
        prompt_responses = {}
        for label_id in label_ids:
            self.cur.execute(f"SELECT prompt, response FROM labels WHERE label_id = {label_id}")
            prompt_responses[label_id] = self.cur.fetchone()
        return prompt_responses
