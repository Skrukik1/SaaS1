import React, { useEffect, useState } from "react";
import axios from "axios";

function UserManagement() {
  const [users, setUsers] = useState([]);
  const [page, setPage] = useState(0);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchUsers();
  }, [page]);

  async function fetchUsers() {
    setError("");
    try {
      const response = await axios.get(`/users?skip=${page * 20}&limit=20`);
      setUsers(response.data);
    } catch (err) {
      setError("Failed to load users.");
    }
  }

  return (
    <div className="user-management">
      <h2>User Management</h2>
      {error && <p style={{color: "red"}}>{error}</p>}
      <table>
        <thead>
          <tr><th>ID</th><th>Username</th><th>Email</th><th>Roles</th></tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.id}</td><td>{user.username}</td><td>{user.email}</td><td>{user.roles.join(", ")}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <button disabled={page === 0} onClick={() => setPage(page - 1)}>Previous</button>
      <button onClick={() => setPage(page + 1)}>Next</button>
    </div>
  );
}

export default UserManagement;
