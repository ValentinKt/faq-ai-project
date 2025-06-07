import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { RootState } from './store';
import FAQList from './components/faq/FAQList';
import AdminDashboard from './components/admin/AdminDashboard';
import Login from './components/auth/Login';

const HomePage: React.FC = () => (
    <div className="container mx-auto p-4">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">FAQ Management System</h1>
        <FAQList />
    </div>
);

interface PrivateRouteProps {
    children: React.ReactNode;
    allowedRoles?: string[];
}

const PrivateRoute: React.FC<PrivateRouteProps> = ({ children, allowedRoles }) => {
    const { isAuthenticated, user } = useSelector((state: RootState) => state.auth);
    if (!isAuthenticated) return <Navigate to="/login" replace />;
    if (allowedRoles && user && !allowedRoles.some(role => user.roles.includes(role))) {
        return <Navigate to="/" replace />;
    }
    return <>{children}</>;
};

const App: React.FC = () => {
    return (
        <Router>
            <div className="min-h-screen bg-gray-100">
                <header className="bg-white shadow-sm p-4">
                    <nav className="container mx-auto flex justify-between items-center">
                        <a href="/" className="text-xl font-bold text-blue-600">FAQ System</a>
                        <div>
                            <a href="/" className="text-gray-700 hover:text-blue-600 mr-4">Home</a>
                            <a href="/admin" className="text-gray-700 hover:text-blue-600 mr-4">Admin</a>
                            <a href="/login" className="text-gray-700 hover:text-blue-600">Login</a>
                        </div>
                    </nav>
                </header>
                <main className="py-8">
                    <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/admin" element={
                            <PrivateRoute allowedRoles={['admin', 'editor']}>
                                <AdminDashboard />
                            </PrivateRoute>
                        } />
                        <Route path="*" element={<Navigate to="/" replace />} />
                    </Routes>
                </main>
            </div>
        </Router>
    );
};

export default App;

