// src/pages/ResumePage.jsx
import React, { useState, useEffect } from 'react';
import { uploadResume, getResumeList, getFeedback,generateResume } from '../api/api';

export default function ResumePage() {
  const [text, setText] = useState('');
  const [resumes, setResumes] = useState([]);
  const [editedText, setEditedText] = useState('');
  const [feedbackText, setFeedbackText] = useState('');
  
  const [company, setCompany] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState('');
  const [years, setYears] = useState('');
  const [experience, setExperience] = useState('');
  const [generatedText, setGeneratedText] = useState('');

  useEffect(() => {
    fetchResumes();
  }, []);

  const fetchResumes = async () => {
    try {
      const res = await getResumeList();
      setResumes(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleUpload = async () => {
    if (!text.trim()) return;
    try {
      await uploadResume(1, text);
      setText('');
      fetchResumes();
    } catch (err) {
      console.error(err);
    }
  };

  const handleFeedback = async (id) => {
    try {
      const res = await getFeedback(id);
      setEditedText(res.data.edited_text);
      setFeedbackText(res.data.feedback);
    } catch (err) {
      console.error(err);
    }
  };

  // 새 자소서 생성 핸들러
  const handleGenerate = async () => {
    if (!company || !name || !role || !years || !experience) return;
    try {
      const res = await generateResume({
        company,                        // 추가
        name,
        role,
        experience_years: Number(years),
        experience_list: experience,
      });
      setGeneratedText(res.data.generated_text);
    } catch (err) {
      console.error(err);
    }
  };

  // 이력서 텍스트에서 첫 두 줄만 추출
  const getPreview = (fullText) => {
    const lines = fullText.split('\n').filter(l => l.trim() !== '');
    const preview = lines.slice(0, 2).join(' ');
    return preview + (lines.length > 2 ? '...' : '');
  };

  return (
    <div>
      <h2 className="mb-4">📝 작성한 이력서 입력</h2>

      <div className="mb-3">
        <textarea
          className="form-control shadow-sm"
          placeholder="이력서 내용을 여기에 붙여넣으세요!"
          rows={6}
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
      </div>
      <button className="btn btn-primary mb-5" onClick={handleUpload}>
        이력서 첨삭
      </button>

      {/* ★ 피드백 카드 먼저 */}
      {(editedText || feedbackText) && (
        <div className="card shadow-sm mb-5">
          <div className="card-body">
            <h4 className="card-title">✏️ 이력서 첨삭 </h4>
            <div
              className="card-text"
              style={{
                whiteSpace: 'pre-wrap',   // 원문 줄바꿈 보존
                overflowX: 'auto'         // 긴 줄은 가로 스크롤
              }}
            >
              {editedText}
            </div>
            
            <h4 className="card-title mt-4">💡 Feedback</h4>
            <p className="card-text">{feedbackText}</p>
          </div>
        </div>
      )}

      <h3 className="mb-3">📂 이력서 히스토리</h3>
      <ul className="list-group mb-4 shadow-sm">
        {resumes.map((res) => (
          <li
            key={res.id}
            className="list-group-item d-flex justify-content-between align-items-start"
          >
            <div>
              <div><strong>ID:</strong> {res.id}</div>
              <div className="text-muted small">
                {getPreview(res.text || res.original_text || '')}
              </div>
            </div>
            <button
              className="btn btn-outline-secondary btn-sm"
              onClick={() => handleFeedback(res.id)}
            >
              피드백 보기
            </button>
          </li>
        ))}
      </ul>

      <hr />
      <h2 className="mb-4"> 👩🏻‍💻 DIY 자기소개서 생성 👩🏻‍💻</h2>
      <div className="row g-3 mb-3">
        <div className="col-md-4">
          <input
            type="text"
            className="form-control shadow-sm"
            placeholder="지원 회사"
            value={company}                // 새로 추가된 state
            onChange={e => setCompany(e.target.value)}
          />
        </div>
        <div className="col-md-6">
          <input
            type="text"
            className="form-control shadow-sm"
            placeholder="이름"
            value={name}
            onChange={e => setName(e.target.value)}
          />
        </div>
        <div className="col-md-6">
          <input
            type="text"
            className="form-control shadow-sm"
            placeholder="희망 직무"
            value={role}
            onChange={e => setRole(e.target.value)}
          />
        </div>
        <div className="col-md-4">
          <input
            type="number"
            className="form-control shadow-sm"
            placeholder="경력 연차"
            value={years}
            onChange={e => setYears(e.target.value)}
          />
        </div>
        <div className="col-md-8">
          <input
            type="text"
            className="form-control shadow-sm"
            placeholder="경력 요약"
            value={experience}
            onChange={e => setExperience(e.target.value)}
          />
        </div>
      </div>
      <button
        className="btn btn-success mb-5"
        onClick={handleGenerate}
        disabled={!name || !role || !years || !experience}
      >
        자기소개서 생성
      </button>
      {generatedText && (
        <div className="mb-5">
          <h5> 👉🏻 생성된 자기소개서</h5>
          <div
            className="p-3 border rounded bg-light"
            style={{
              whiteSpace: 'pre-wrap',
              overflowY: 'auto',
              maxHeight: '400px'   // 원하는 최대 높이 설정
            }}
          >
            {generatedText}
          </div>
        </div>
      )}
    </div>        
  );                
}