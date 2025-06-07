import React, { useState } from 'react';
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/react/24/outline';
import { AnalyticsService } from '../../services/analytics';
import { FAQ } from '../../types';

interface FAQItemProps {
    faq: FAQ;
    isOpen: boolean;
    onClick: () => void;
}

const FAQItem: React.FC<FAQItemProps> = ({ faq, isOpen, onClick }) => {
    const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);

    const handleFeedback = async (helpful: boolean) => {
        try {
            await AnalyticsService.logFAQFeedback(faq.id, { isHelpful: helpful });
            setFeedbackSubmitted(true);
        } catch (error) {
            console.error('Feedback submission failed:', error);
        }
    };

    return (
        <div className={`border border-gray-200 rounded-xl overflow-hidden transition-all duration-300 hover:shadow-md ${isOpen ? 'bg-blue-50' : 'bg-white'}`}>
            <div
                className="flex justify-between items-center p-5 cursor-pointer"
                onClick={onClick}
                onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') onClick(); }}
                role="button"
                tabIndex={0}
                aria-expanded={isOpen}
                aria-controls={`faq-content-${faq.id}`}
            >
                <h3 className="font-medium text-gray-800">{faq.question}</h3>
                {isOpen ? <ChevronUpIcon className="h-5 w-5 text-blue-600" /> : <ChevronDownIcon className="h-5 w-5 text-gray-500" />}
            </div>
            {isOpen && (
                <div id={`faq-content-${faq.id}`} className="p-5 bg-gray-50 border-t border-gray-100 animate-fade-in">
                    <div className="prose max-w-none text-gray-600" dangerouslySetInnerHTML={{ __html: faq.answer }} />
                    <div className="mt-6 pt-4 border-t border-gray-200 flex items-center justify-end">
                        {!feedbackSubmitted ? (
                            <div className="flex space-x-3">
                                <button
                                    onClick={() => handleFeedback(true)}
                                    className="flex items-center text-sm text-green-600 hover:text-green-800"
                                    aria-label="Mark as helpful"
                                >
                                    <svg className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905a3.61 3.61 0 01-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                                    </svg>
                                    Helpful
                                </button>
                                <button
                                    onClick={() => handleFeedback(false)}
                                    className="flex items-center text-sm text-red-600 hover:text-red-800"
                                    aria-label="Mark as not helpful"
                                >
                                    <svg className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14H5.236a2 2 0 01-1.789-2.894l-3.5-7A2 2 0 018.736 3h4.018c.163 0 .326.02.485.06L17 4m0 0v9m0-9h2.765a2 2 0 011.789 2.894l-3.5 7A2 2 0 0118.264 15H17m0 0h-2M7 10h.01M17 14h.01" />
                                    </svg>
                                    Not helpful
                                </button>
                            </div>
                        ) : (
                            <p className="text-sm text-gray-500">Thank you for your feedback!</p>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default FAQItem;