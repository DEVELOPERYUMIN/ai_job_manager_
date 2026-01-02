import React, { useState, useEffect } from 'react';
import { getResumeList, getFeedback } from '../api/api';

export default function DashboardPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      const res = await getResumeList();
      const data = await Promise.all(
        res.data.map(async (r) => {
          const fb = await getFeedback(r.id);
          return {
            id: r.id,
            original: r.text,
            edited: fb.data.edited_text,
            feedback: fb.data.feedback,
          };
        })
      );
      setItems(data);
      setLoading(false);
    })();
  }, []);

  if (loading) {
    return <div className="text-center py-5">Loading...</div>;
  }

  return (
    <div>
      <h2 className="mb-4">📊 나의 취준 기록</h2>
      <table className="table table-striped table-hover shadow-sm">
        <thead className="table-light">
          <tr>
            <th>ID</th>
            <th>Edited</th>
            <th>Feedback</th>
          </tr>
        </thead>
        <tbody>
          {items.map((it) => (
            <tr key={it.id}>
              <td>{it.id}</td>
              <td>{it.edited}</td>
              <td>{it.feedback}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

