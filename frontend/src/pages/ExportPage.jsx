
import React, { useState } from 'react';
import {
  requestExportDocx,
  requestExportPdf,
  downloadDocx,
  downloadPdf,
} from '../api/api';

export default function ExportPage() {
  const [loading, setLoading] = useState(false);

  const handleExport = async (type) => {
    setLoading(true);
    try {
      // 1) 리포트 생성 → filename 받기
      const exportRes =
        type === 'docx'
          ? await requestExportDocx(1)
          : await requestExportPdf(1);
      const { filename } = exportRes.data;

      // 2) 실제 파일 다운로드 (blob)
      const fileRes =
        type === 'docx'
          ? await downloadDocx(filename)
          : await downloadPdf(filename);

      const blob = new Blob([fileRes.data], {
        type: fileRes.headers['content-type'],
      });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div>
      <h2 className="mb-4">📥 취준 히스토리 다운로드</h2>

      <div className="row g-3 mb-5">
        <div className="col-md-5">
          <button
            className="btn btn-outline-primary w-100"
            disabled={loading}
            onClick={() => handleExport('docx')}
          >
            DOCX로 다운로드
          </button>
        </div>
        <div className="col-md-5">
          <button
            className="btn btn-outline-success w-100"
            disabled={loading}
            onClick={() => handleExport('pdf')}
          >
            PDF로 다운로드 
          </button>
        </div>
        <div className="col-md-2 d-flex align-items-center">
          {loading && (
            <span className="text-muted">파일 생성/다운로드 중…</span>
          )}
        </div>
      </div>
    </div>
  );
}
