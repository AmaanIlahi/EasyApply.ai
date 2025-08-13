import Link from 'next/link';
import styles from '@/styles/layout.module.scss';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';

const Header = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [showDropdown, setShowDropdown] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');

    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        setUsername(payload.sub || '');
        setIsLoggedIn(true);
      } catch (err) {
        console.error('Invalid token', err);
        setIsLoggedIn(false);
      }
    } else {
      setIsLoggedIn(false);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    router.push('/login');
  };

  const handleNavigation = (path: string) => {
    if (!isLoggedIn) {
      router.push('/login');
    } else {
      router.push(path);
    }
    setShowDropdown(false);
  };

  return (
    <header className={styles.header}>
      <div className={styles.logo}>
        <Link href="/">EasyApply.ai</Link>
      </div>
      <nav className={styles.nav}>
        {isLoggedIn ? (
          <div className={styles.userMenu}>
            <span>Welcome, {username} 👤</span>
            <button
              className={styles.menuButton}
              onClick={() => setShowDropdown((prev) => !prev)}
            >
              ☰
            </button>
            {showDropdown && (
              <div className={styles.dropdown}>
                <button onClick={() => handleNavigation('/submit-document')}>
                  Submit Document
                </button>
                <button onClick={() => handleNavigation('/ats-score')}>
                  ATS Score Match
                </button>
                <button onClick={() => handleNavigation('/generate-cover-letter')}>
                  Cover Letter
                </button>
                <button onClick={handleLogout}>Logout</button>
              </div>
            )}
          </div>
        ) : (
          <>
            <Link href="/signup">Sign Up</Link>
            <Link href="/login">Login</Link>
          </>
        )}
      </nav>
    </header>
  );
};

export default Header;
