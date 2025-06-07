import { useEffect } from 'react';
import { FAQ } from '../../types';
import React, { useState } from'react';
import { FAQService } from '../../services/api';



export const FAQPage: React.FC = () => {
  const [faqs, setFaqs] = useState<FAQ[]>([]);
  const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);


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


  const handleFAQClick = (faq: FAQ) => {
    // Handle click logic

    // Example: Toggle the 'isOpen' property of the clicked FAQ
    const updatedFaqs = faqs.map((f) =>
      f.id === faq.id ? { ...f, expanded: !f.expanded } : f
    );
    setFaqs(updatedFaqs);

  };

  return (
    <div className="h-[calc(100vh-200px)]">
      {loading ? (
        <div>Loading...</div>
      ) : error ? (
        <div>{error}</div>
      ) : (
        //<FAQList faqs={faqs} onFAQClick={handleFAQClick} />
        // ERROR: Element type is invalid: expected a string (for built-in components) or a class/function (for composite components) but got: undefined. You likely forgot to export your component from the file it's defined in, or you might have mixed up default and named imports.
        <div className="space-y-4">
          {faqs.map((faq) => (
            <div 
              key={faq.id}
              className="border rounded p-4 cursor-pointer"
              onClick={() => handleFAQClick(faq)}
            >
              <h3 className="font-medium">{faq.question}</h3>
              {faq.expanded && (
                <p className="mt-2">{faq.answer}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};