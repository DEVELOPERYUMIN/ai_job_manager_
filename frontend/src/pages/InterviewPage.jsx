// src/pages/InterviewPage.jsx
import React, { useState } from 'react';
import {
  generateQuestions,    // POST /interviews/questions
  saveAnswer,           // POST /interviews/answers
  evaluateAnswer        // POST /interviews/evaluate/{answer_id}
} from '../api/api';

export default function InterviewPage() {
  const [company, setCompany] = useState('');
  const [role, setRole] = useState('');
  const [questions, setQuestions] = useState([]);

  const handleGenerate = async () => {
    if (!company.trim() || !role.trim()) {
      alert('Company와 Role을 모두 입력하세요.');
      return;
    }
    try {
      const res = await generateQuestions({ user_id: 1, company, role });
      // API로부터 받은 [{id, text}]를
      // UI용으로 확장된 객체로 변환
      const formatted = (res.data.questions || []).map((q) => ({
        id: q.id,
        text: q.text ?? q.question ?? q, // 유연하게 처리
        userAnswer: '',
        answerSaved: false,
        answerId: null,
        evaluation: null,
      }));
      setQuestions(formatted);
    } catch (err) {
      console.error('❌ 질문 생성 실패', err);
      alert('질문 생성에 실패했습니다.');
    }
  };

  const handleSave = async (q, idx) => {
    if (!q.userAnswer.trim()) {
      alert('먼저 답변을 입력하세요.');
      return;
    }
    try {
      const payload = {
        question_id: q.id,
        answer_text: q.userAnswer.trim(),
      };
      const res = await saveAnswer(payload);
      const updated = [...questions];
      updated[idx] = {
        ...q,
        answerSaved: true,
        answerId: res.data.id,
      };
      setQuestions(updated);
    } catch (err) {
      console.error('❌ 답변 저장 실패', err);
      alert('답변 저장에 실패했습니다.');
    }
  };

  const handleEvaluate = async (q, idx) => {
    if (!q.answerSaved) {
      alert('먼저 Save 버튼을 눌러주세요.');
      return;
    }
    try {
      const res = await evaluateAnswer(q.answerId, { answer_text: q.userAnswer });
      const updated = [...questions];
      updated[idx] = {
        ...q,
        evaluation: res.data,
      };
      setQuestions(updated);
    } catch (err) {
      console.error('❌ 평가 실패', err);
      alert('평가에 실패했습니다.');
    }
  };

  return (
    <div className="container py-4">
      <h2 className="mb-4">🎤 모의 면접</h2>

      {/* Input row */}
      <div className="row g-3 mb-5">
        <div className="col-md-5">
          <input
            type="text"
            className="form-control shadow-sm"
            placeholder="지원할 회사"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
          />
        </div>
        <div className="col-md-5">
          <input
            type="text"
            className="form-control shadow-sm"
            placeholder="지원할 직무"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          />
        </div>
        <div className="col-md-2">
          <button
            className="btn btn-success w-100"
            onClick={handleGenerate}
          >
            질문생성
          </button>
        </div>
      </div>

      {/* Questions list */}
      <ul className="list-group mb-4 shadow-sm">
        {questions.length === 0 && (
          <li className="list-group-item text-muted">
            질문이 없습니다. Generate를 눌러주세요.
          </li>
        )}
        {questions.map((q, idx) => (
          <li key={q.id} className="list-group-item">
            <p className="mb-2"><strong>Q:</strong> {q.text}</p>
            <textarea
              className="form-control mb-3"
              rows={3}
              value={q.userAnswer}
              onChange={(e) => {
                const updated = [...questions];
                updated[idx] = { ...q, userAnswer: e.target.value };
                setQuestions(updated);
              }}
            />
            <div className="d-flex gap-2">
              <button
                className={`btn btn-outline-primary btn-sm${q.answerSaved ? ' disabled' : ''}`}
                onClick={() => handleSave(q, idx)}
              >
                {q.answerSaved ? 'Saved' : 'Save'}
              </button>
              <button
                className="btn btn-outline-info btn-sm"
                onClick={() => handleEvaluate(q, idx)}
              >
                Evaluate
              </button>
            </div>
            {q.evaluation && (
              <div className="mt-3 p-3 border rounded bg-light">
                <h6>📝 Evaluation</h6>
                <p className="mb-1"><strong>Score:</strong> {q.evaluation.score}</p>
                <p className="mb-0"><strong>Feedback:</strong> {q.evaluation.feedback}</p>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
