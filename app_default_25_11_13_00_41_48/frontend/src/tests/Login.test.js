import { render, screen, fireEvent } from "@testing-library/react";
import Login from "../components/Auth/Login";
import axios from "axios";

jest.mock("axios");

describe("Login component", () => {
  it("renders login form", () => {
    render(<Login />);
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  });

  it("validates empty form", () => {
    render(<Login />);
    fireEvent.click(screen.getByText(/log in/i));
    expect(screen.getByText(/username and password are required/i)).toBeInTheDocument();
  });

  it("submits form successfully", async () => {
    axios.post.mockResolvedValue({ data: { access_token: "token" } });
    render(<Login />);
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: "testuser" } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: "password123" } });
    fireEvent.click(screen.getByText(/log in/i));
    // Wait for redirect or token set
  });

  it("shows error on invalid credentials", async () => {
    axios.post.mockRejectedValue(new Error("Invalid"));
    render(<Login />);
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: "baduser" } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: "badpass" } });
    fireEvent.click(screen.getByText(/log in/i));
    // Expect error message to appear
  });
});
