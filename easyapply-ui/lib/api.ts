import axios from 'axios';

// lib/api.ts
const API_URL = 'http://localhost:8000';

export async function login(data: { username: string; password: string }) {

  // console.log('[Login] Sending data:', data); // Debug input
  const res = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  // console.log('[Login] Response status:', res.status); // Debug response status
  if (!res.ok) {
    throw new Error('Login failed');
  }

  const result = await res.json(); // Expecting { access_token, token_type }
  return result;
}


/**
 * Submit Document API - via manual input or file
 */
export async function submitDocument({
  manualInput,
  file,
  token,
}: {
  manualInput?: string;
  file?: File;
  token: string;
}) {
  const formData = new FormData();

  if (manualInput) formData.append('manual_input', manualInput);
  if (file) formData.append('file', file);

  console.log('[Submit] Sending form data:', {
    hasManualInput: !!manualInput,
    hasFile: !!file,
  });

  try {
    const response = await axios.post(`${API_URL}/resume/submit-document`, formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data',
      },
    });

    console.log('[Submit] Success response:', response.data);
    return response.data;
  } catch (error: any) {

    const status = error.response?.status;
    const message = error.response?.data?.detail || error.message;

    if (status === 401) {
      throw new Error('TokenExpired'); // Special error string
    }

    console.error('[Submit] Error:', message);
    throw new Error(message || 'Failed to submit document');
  }
}


export async function generateCoverLetter(jobDescription: string, token: string): Promise<string> {
  const response = await fetch(`${API_URL}/coverletter/generate-cover-letter`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ job_description: jobDescription }),
  });

  if (response.status === 401) {
    throw new Error('unauthorized');
  }

  if (!response.ok) {
    throw new Error('Failed to generate cover letter');
  }

  const data = await response.json();
  return data.cover_letter;
}