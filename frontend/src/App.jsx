import React, { useState, useEffect } from 'react';
import { db } from './firebase'; 
import { collection, getDocs } from 'firebase/firestore';

function App() {
  const [search, setSearch] = useState("");
  const [currentApp, setCurrentApp] = useState(null);
  const [selectedVersion, setSelectedVersion] = useState("");
  const [loading, setLoading] = useState(false);

  // 1. Fonction de recherche de l'application
  const handleSearch = async () => {
    setLoading(true);
    setSelectedVersion(""); // Reset la version lors d'une nouvelle recherche
    const querySnapshot = await getDocs(collection(db, "applications"));
    const apps = querySnapshot.docs.map(doc => doc.data());
    const match = apps.find(a => a.application.toLowerCase() === search.toLowerCase());
    setCurrentApp(match);
    setLoading(false);
  };

  // 2. Extraire les versions uniques disponibles pour cette application
  const availableVersions = currentApp 
    ? [...new Set(currentApp.solutions.map(s => s.version).filter(Boolean))] 
    : [];

  // 3. Filtrer les solutions selon la version choisie
  const filteredSolutions = currentApp 
    ? currentApp.solutions.filter(s => !selectedVersion || s.version === selectedVersion)
    : [];

  return (
    <div className="min-h-screen bg-black text-white p-8 font-mono">
      <h1 className="text-4xl mb-8 text-green-500 font-bold underline">EXIT0.TECH</h1>
      
      <div className="flex gap-4 mb-8">
        <input 
          value={search} 
          onChange={(e) => setSearch(e.target.value)}
          placeholder="TYPE_APP_NAME (ex: linux, docker...)"
          className="bg-black border-2 border-green-500 p-2 w-64 text-green-400 outline-none"
        />
        <button onClick={handleSearch} className="bg-green-600 px-6 py-2 hover:bg-green-400 transition-colors font-bold">
          RUN_SEARCH
        </button>
      </div>

      {/* SÉLECTEUR DE VERSION (Nouveau) */}
      {currentApp && availableVersions.length > 0 && (
        <div className="mb-12 p-4 border border-zinc-800 bg-zinc-900/50 rounded-lg animate-fade-in">
          <label className="text-green-500 block mb-2 font-bold">> SELECT_TARGET_VERSION:</label>
          <select 
            value={selectedVersion}
            onChange={(e) => setSelectedVersion(e.target.value)}
            className="bg-black border border-green-500 text-white p-2 w-full max-w-md outline-none cursor-pointer"
          >
            <option value="">-- ALL VERSIONS --</option>
            {availableVersions.map(v => (
              <option key={v} value={v}>{v}</option>
            ))}
          </select>
        </div>
      )}

      {currentApp && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredSolutions.map((sol, index) => (
            <div key={index} className="border border-green-900 p-4 bg-zinc-900 shadow-lg relative overflow-hidden group">
              <div className="flex justify-between items-start mb-4">
                <p className="text-[10px] text-zinc-500 italic">AUTHOR: {sol.author}</p>
                {sol.version && (
                  <span className="text-[10px] bg-green-900/50 text-green-400 px-2 py-0.5 border border-green-500/30">
                    VER: {sol.version}
                  </span>
                )}
              </div>
              
              {sol.blocks.map((block, i) => (
                <div key={i} className="mb-4">
                  {block.type === 'text' ? 
                    <p className="text-sm leading-relaxed text-zinc-300">{block.content}</p> : 
                    <div className="relative">
                      <pre className="bg-black p-3 text-green-300 text-sm overflow-x-auto border-l-2 border-green-600">
                        <code>{block.content}</code>
                      </pre>
                    </div>
                  }
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
