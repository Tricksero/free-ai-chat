// src/app/add/page.js

"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Todo } from "../page";

/**
 * Sends a POST request to create a new menu item.
 * @param {Object} data The menu item data to be sent.
 */
async function createMenu(data: Todo) {
  const res = await fetch("http://127.0.0.1:8000/api/todo/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    throw new Error("Failed to create data");
  }

  return res.json();
}

const Page = () => {
  const router = useRouter();
  const [formData, setFormData] = useState({ name: "", desc: "" });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string|null>(null);

  /**
   * Handles the form submission.
   * @param {Event} event The form submission event.
   */
  const onFinish = (event: React.FormEvent) => {
    event.preventDefault();
    setIsLoading(true);
    createMenu(formData)
      .then(() => {
        // Navigate to the main page with a query parameter indicating success
        router.replace("/?action=add");
      })
      .catch(() => {
        setError("An error occurred");
        setIsLoading(false);
      });
  };

  // Cleanup effect for resetting loading state
  useEffect(() => {
    return () => setIsLoading(false);
  }, []);

  return (
    <form onSubmit={onFinish}>
      <div className="form-item">
        <label htmlFor="name">Name</label>
        <input
          required
          name="name"
          value={formData.name}
          onChange={(event) =>
            setFormData({ ...formData, name: event.target.value })
          }
        />
      </div>
      <div className="form-item">
        <label htmlFor="desc">Description</label>
        <input
          required
          name="name"
          value={formData.desc}
          onChange={(event) =>
            setFormData({ ...formData, desc: event.target.value })
          }
        />
      </div>
      {error && <p className="error-message">{error}</p>}
      <div>
        <button disabled={isLoading} className="add-button" type="submit">
          Submit
        </button>
      </div>
    </form>
  );
};

export default Page;