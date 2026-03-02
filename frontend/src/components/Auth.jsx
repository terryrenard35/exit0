import React from 'react';
import { auth, googleProvider } from '../firebase';
import { signInWithPopup, signOut } from 'firebase/auth';
import { useAuth } from '../hooks/useAuth';

const Auth = () => {
  const { user, loading } = useAuth();

  if (loading) return <div className="animate-pulse text-gray-500">...</div>;

  return (
    <div className="flex items-center gap-4">
      {user ? (
        <div className="flex items-center gap-3 bg-gray-800 p-2 rounded-lg border border-gray-700">
          <div className="flex flex-col items-end">
            <span className="text-sm font-bold text-white">{user.displayName}</span>
            <span className="text-xs text-blue-400 font-mono">🎖️ {user.badges[0]}</span>
          </div>
          <button 
            onClick={() => signOut(auth)}
            className="bg-red-900/50 hover:bg-red-800 text-red-200 text-xs py-1 px-3 rounded border border-red-700 transition-all"
          >
            Sortie
          </button>
        </div>
      ) : (
        <button 
          onClick={() => signInWithPopup(auth, googleProvider)}
          className="bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded-lg flex items-center gap-2 transition-transform active:scale-95 shadow-lg"
        >
          <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" className="w-5 h-5 bg-white rounded-full p-0.5" alt="G" />
          Connexion IT
        </button>
      )}
    </div>
  );
};

export default Auth;
