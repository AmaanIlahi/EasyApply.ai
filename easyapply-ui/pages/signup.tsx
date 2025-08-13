import { useForm } from 'react-hook-form';
import { signup } from '@/lib/api';
import { useRouter } from 'next/router';
import styles from '@/styles/Form.module.scss';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

export default function SignupPage() {
  const { register, handleSubmit } = useForm();
  const router = useRouter();

  const onSubmit = async (data: any) => {
    try {
      await signup(data);
      router.push('/login');
    } catch {
      alert('Signup failed');
    }
  };

  return (
    <>
      <Header />
      <main className={styles.formContainer}>
        <form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
          <h2>Sign Up</h2>
          <input {...register('first_name')} placeholder="First Name" required />
          <input {...register('last_name')} placeholder="Last Name" required />
          <input {...register('username')} placeholder="Username" required />
          <input type="password" {...register('password')} placeholder="Password" required />
          <button type="submit">Sign Up</button>
        </form>
      </main>
      <Footer />
    </>
  );
}
