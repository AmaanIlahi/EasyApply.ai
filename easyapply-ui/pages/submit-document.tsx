import { useForm } from 'react-hook-form';
import { useState } from 'react';
import { submitDocument } from '@/lib/api';
import styles from '@/styles/Form.module.scss';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

export default function SubmitDocumentPage() {
  const { register, handleSubmit, reset } = useForm();
  const [summary, setSummary] = useState<string | null>(null);

  const onSubmit = async (data: any) => {
    const token = localStorage.getItem('token') || '';
    if (!token) {
      alert('You must be logged in to submit a document.');
      return;
    }

    const file = data.file?.[0];
    const manualInput = data.manual_input;

    try {
      const response = await submitDocument({ manualInput, file, token });
      setSummary(response.cleaned_text);
      reset();
    } catch (error) {
        if (error.message === 'TokenExpired') {
          alert('Session expired. Please log in again.');
          localStorage.removeItem('token');
          router.push('/login');
        } else {
          alert(error.message || 'Submit failed');
        }
    }
  };

  return (
    <>
      <Header />
      <form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
        <h2>Submit Resume</h2>
        <textarea
          {...register('manual_input')}
          placeholder="Paste resume here..."
          rows={8}
        />
        <p style={{ textAlign: 'center', margin: '1rem 0' }}>— OR —</p>
        <input type="file" accept=".pdf,.doc,.docx,.txt" {...register('file')} />
        <button type="submit">Submit</button>

        {summary && (
        <div className={styles.summary}>
          <h3>Cleaned Summary</h3>
          <p>{summary}</p>
        </div>
      )}
      </form>

      
      <Footer />
    </>
  );
}
