
const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const path = require("path");

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

const db = new sqlite3.Database(":memory:");

db.serialize(() => {
  db.run(`
    CREATE TABLE users (
      id INTEGER PRIMARY KEY,
      username TEXT NOT NULL,
      password TEXT NOT NULL,
      role TEXT NOT NULL
    )
  `);

  const insert = db.prepare(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)"
  );

  insert.run("alice", "alice123", "user");
  insert.run("bob", "bob123", "user");
  insert.finalize();
});

function queryOne(sql, params = []) {
  return new Promise((resolve, reject) => {
    db.get(sql, params, (err, row) => {
      if (err) return reject(err);
      resolve(row || null);
    });
  });
}

// INTENTIONALLY VULNERABLE: coursework demonstration
app.post("/api/login", async (req, res) => {
  const username = String(req.body.username ?? "");
  const password = String(req.body.password ?? "");

  // VULNERABLE QUERY: input is concatenated into SQL.
//   const sql =
//     `SELECT id, username, role FROM users ` +
//     `WHERE username = '${username}' AND password = '${password}'`;

    const sql =
  "SELECT id, username, role FROM users WHERE username = ? AND password = ?";


  try {
    // const user = await queryOne(sql);

    const user = await queryOne(sql, [username, password]);

    if (!user) {
      return res.status(401).json({
        authenticated: false,
        message: "Invalid username or password."
      });
    }

    return res.json({
      authenticated: true,
      message: `Welcome, ${user.username}!`,
      user: {
        username: user.username,
        role: user.role
      }
    });
  } catch (err) {
    return res.status(400).json({
      authenticated: false,
      message: "Login could not be processed."
    });
  }
});

app.listen(PORT, "127.0.0.1", () => {
  console.log(`Application running at http://127.0.0.1:${PORT}`);
  console.log("Control account: alice / alice123");
});
