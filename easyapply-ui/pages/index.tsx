import Header from '@/components/Header';
import Footer from '@/components/Footer';
import styles from '@/styles/layout.module.scss';

export default function Home() {
  const isLoggedIn = false; // You can later manage this via state or context
  const username = 'Amaan';

  return (
    <>
      <Header isLoggedIn={isLoggedIn} username={username} />
      <main className={styles.main}>
        <h1>Welcome to EasyApply.ai</h1>
        <p>
          Your AI-powered assistant to simplify job applications with resume parsing, cover letter
          generation, and smart document management.
        </p>
      </main>
      <Footer />
    </>
  );
}
