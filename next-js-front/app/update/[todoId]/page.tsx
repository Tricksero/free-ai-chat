// src/app/update/[menuId]/page.js

"use client"

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Todo } from "@/app/page";

/**
 * Fetches a menu item by ID.
 * @param {number} id The ID of the menu item to retrieve.
 */
async function getTodo(id: number) {
  const res = await fetch(`http://127.0.0.1:8000/api/todo/${id}/`);
  if (!res.ok) {
    throw new Error("Failed to retrieve menu");
  }
  return res.json();
}

/**
 * Updates a menu item by ID.
 * @param {number} id The ID of the menu item to update.
 * @param {Object} data The updated data for the menu item.
 */
async function updateTodo(id: number, data: Todo) {
  const res = await fetch(`http://127.0.0.1:8000/api/todo/${id}/`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    throw new Error("Failed to update menu");
  }
  return res.json();
}

const Page: React.FC<any> = ({ params }) => {
  const router = useRouter();
  const [formData, setFormData] = useState<Todo>({ name: "", desc: "" });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string|null>(null);

  /**
   * Handles form submission.
   * @param {Event} event The form submission event.
   */
  const onFinish = (event: React.FormEvent) => {
    event.preventDefault();
    setIsLoading(true);
    updateTodo(params.menuId, formData)
      .then(() => {
        router.replace("/?action=update");
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

  // Fetch menu item data on component mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getTodo(params.todoId);
        setFormData({ name: data.name, desc: data.desc });
      } catch (error: any) {
        setError(error.message);
      }
    };
    fetchData();
  }, [params.todoId]);

  return (
    <form onSubmit={onFinish}>
      <div className="form-item">
        <label htmlFor="name">Name</label>
        <input
          required
          name="name"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
        />
      </div>
      <div className="form-item">
        <label htmlFor="desc">Description</label>
        <input
          required
          name="desc"
          value={formData.desc}
          onChange={(e) => setFormData({ ...formData, desc: e.target.value })}
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