import { useState } from 'react';
import styles from '@/styles/Form.module.scss';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { generateCoverLetter } from '@/lib/api';

export default function GenerateCoverLetterPage() {
  const [jobDescription, setJobDescription] = useState('');
  const [coverLetter, setCoverLetter] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    const token = localStorage.getItem('token');

    if (!token) {
      alert('Please log in first.');
      window.location.href = '/login';
      return;
    }

    try {
      const result = await generateCoverLetter(jobDescription, token);
      setCoverLetter(result);
    } catch (error: any) {
      if (error.message === 'unauthorized') {
        alert('Session expired. Please log in again.');
        localStorage.removeItem('token');
        window.location.href = '/login';
      } else {
        alert('Error generating cover letter.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Header />
      <div className={styles.form}>
        <h2>Generate Cover Letter</h2>
        <textarea
          rows={8}
          placeholder="Paste the job description here..."
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
        />
        <button onClick={handleGenerate} disabled={loading}>
          {loading ? 'Generating...' : 'Generate Cover Letter'}
        </button>

        {coverLetter && (
          <div className={styles.form}>
            <h3>Your Cover Letter</h3>
            <pre>{coverLetter}</pre>
          </div>
        )}
      </div>
      <Footer />
    </>
  );
}
