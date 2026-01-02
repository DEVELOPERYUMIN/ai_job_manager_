import axios from 'axios';
const API = axios.create();
export const uploadResume    = (user_id, text)   => API.post('/resumes', { user_id, text });
export const getResumeList   = ()                => API.get('/resumes');
export const getFeedback     = (id)              => API.post(`/resumes/${id}/feedback`, {});
export const generateResume = ({ name, role, experience_years, experience_list }) =>
  API.post(
    '/resumes/generate',
    { name, role, experience_years, experience_list }
  );

// 면접 질문 생성
export function generateQuestions(payload) {
  return API.post('/interviews/questions', payload);
}

// 답변 저장
export function saveAnswer(payload) {
  return API.post('/interviews/answers', payload);
}

// 답변 평가
export function evaluateAnswer(answerId, payload) {
  return API.post(`/interviews/evaluate/${answerId}`, payload);
}

export const getDashboard      = (user_id)       => API.get(`/dashboard/${user_id}`);


// 기존 export들…
export const requestExportDocx = user_id => API.get(`/exporter/${user_id}/docx`);
export const requestExportPdf  = user_id => API.get(`/exporter/${user_id}/pdf`);

// 여기에 추가하세요!
export const downloadDocx = filename =>
  API.get(`/exporter/download/docx/${filename}`, { responseType: 'blob' });

export const downloadPdf = filename =>
  API.get(`/exporter/download/pdf/${filename}`, { responseType: 'blob' });

export default API;


