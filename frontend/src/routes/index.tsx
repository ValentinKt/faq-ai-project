import { BrowserRouter, Routes, Route } from 'react-router-dom';
import {FAQPage} from '../components/faq/FAQPage';
import AdminDashboard from '../components/admin/AdminDashboard';

const AppRoutes = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/faq" element={<FAQPage />} />
      <Route path="/admin" element={<AdminDashboard />} />
    </Routes>
  </BrowserRouter>
);

export default AppRoutes;