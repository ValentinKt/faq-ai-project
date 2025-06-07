import React, { useState, useEffect } from 'react';
import FAQItem from './FAQItem';
import { FAQService } from '../../services/api';
import { FAQ } from '../../types';

const FAQList: React.FC = () => {
    const [faqs, setFaqs] = useState<FAQ[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [openFaqId, setOpenFaqId] = useState<string | null>(null);

    useEffect(() => {
        const fetchFaqs = async () => {
            try {
                const response = await FAQService.getAll();
                setFaqs((response as any) as FAQ[]);
            } catch (err) {
                setError('Failed to load FAQs');
            } finally {
                setLoading(false);
            }
        };
        fetchFaqs();
    }, []);

    if (loading) return <p className="text-gray-600">Loading FAQs...</p>;
    if (error) return <p className="text-red-600">{error}</p>;

    return (
        <div className="space-y-4">
            {faqs.map(faq => (
                <FAQItem
                    key={faq.id}
                    faq={faq}
                    isOpen={openFaqId === faq.id}
                    onClick={() => setOpenFaqId(openFaqId === faq.id ? null : faq.id)}
                />
            ))}
        </div>
    );
};

export default FAQList;