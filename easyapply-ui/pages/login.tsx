import { useForm } from 'react-hook-form';
import { login } from '@/lib/api';
import { useRouter } from 'next/router';
import styles from '@/styles/Form.module.scss';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

export default function LoginPage() {
  const { register, handleSubmit } = useForm();
  const router = useRouter();

  const onSubmit = async (data: any) => {
    try 
    {
      const response = await login(data); // Gets { access_token, token_type }
      localStorage.setItem('token', response.access_token); // Store token locally
      router.push('/submit-document'); // Redirect on success
    } 
    catch (error) 
    {
      alert('Login failed');
    }
  };

  return (
    <>
      <Header />
      <form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
        <h2>Login</h2>
        <input {...register('username')} placeholder="Username" required />
        <input type="password" {...register('password')} placeholder="Password" required />
        <button type="submit">Login</button>
      </form>
      <Footer />
    </>
  );
}
