import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { listDocuments as getDocuments, listConversations as getConversations } from '../api/client';
import { Document, Conversation } from '../types';
import { toast } from 'react-toastify';

const Dashboard: React.FC = () => {
  const [documentCount, setDocumentCount] = useState<number>(0);
  const [conversationCount, setConversationCount] = useState<number>(0);
  const [recentDocuments, setRecentDocuments] = useState<Document[]>([]);
  const [recentConversations, setRecentConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const [documentsResponse, conversationsResponse] = await Promise.all([
          getDocuments(),
          getConversations(),
        ]);

        setDocumentCount(documentsResponse.length);
        setConversationCount(conversationsResponse.length);

        setRecentDocuments(documentsResponse.slice(0, 5));
        setRecentConversations(conversationsResponse.slice(0, 5));
      } catch (err) {
        setError('Failed to fetch data. Please try again.');
        toast.error('Failed to fetch data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleUploadClick = () => {
    navigate('/upload');
  };

  const handleChatClick = () => {
    navigate('/chat');
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-lg font-semibold">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-red-500 text-lg font-semibold">{error}</div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <div className="bg-white shadow-md rounded-lg p-4">
          <h2 className="text-lg font-semibold">Documents</h2>
          <p className="text-2xl font-bold">{documentCount}</p>
        </div>
        <div className="bg-white shadow-md rounded-lg p-4">
          <h2 className="text-lg font-semibold">Conversations</h2>
          <p className="text-2xl font-bold">{conversationCount}</p>
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Recent Documents</h2>
        <ul className="bg-white shadow-md rounded-lg p-4">
          {recentDocuments.map((doc) => (
            <li key={doc.id} className="border-b last:border-b-0 py-2">
              {doc.name}
            </li>
          ))}
        </ul>
      </div>

      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Recent Conversations</h2>
        <ul className="bg-white shadow-md rounded-lg p-4">
          {recentConversations.map((conv) => (
            <li key={conv.id} className="border-b last:border-b-0 py-2">
              {conv.title}
            </li>
          ))}
        </ul>
      </div>

      <div className="flex space-x-4">
        <button
          onClick={handleUploadClick}
          className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
        >
          Upload Document
        </button>
        <button
          onClick={handleChatClick}
          className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600"
        >
          Start Chat
        </button>
      </div>
    </div>
  );
};

export default Dashboard;