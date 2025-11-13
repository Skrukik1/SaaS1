import { render, screen, waitFor } from "@testing-library/react";
import UserManagement from "../components/Admin/UserManagement";
import axios from "axios";

jest.mock("axios");

describe("UserManagement component", () => {
  it("fetches and displays users", async () => {
    axios.get.mockResolvedValue({
      data: [
        { id: 1, username: "user1", email: "user1@example.com", roles: ["user"] },
        { id: 2, username: "user2", email: "user2@example.com", roles: ["admin"] },
      ],
    });
    render(<UserManagement />);
    await waitFor(() => {
      expect(screen.getByText("user1")).toBeInTheDocument();
      expect(screen.getByText("user2")).toBeInTheDocument();
    });
  });

  it("shows error message on fetch failure", async () => {
    axios.get.mockRejectedValue(new Error("Failed"));
    render(<UserManagement />);
    await waitFor(() => {
      expect(screen.getByText(/failed to load users/i)).toBeInTheDocument();
    });
  });
});
