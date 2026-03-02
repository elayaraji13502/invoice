import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Eye, ExternalLink } from 'lucide-react';
import { Invoice } from '@/types';
import { getReviewQueue } from '@/services/invoiceService';
import PageHeader from '@/components/dashboard/PageHeader';
import DataTable, { Column } from '@/components/dashboard/DataTable';
import StatusBadge from '@/components/dashboard/StatusBadge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { format } from '@/lib/dateUtils';
import { API_BASE_URL } from '@/services/api';

const ReviewQueue: React.FC = () => {
  const navigate = useNavigate();

  const { data: invoices, isLoading } = useQuery({
    queryKey: ['reviewQueue'],
    queryFn: getReviewQueue,
  });

  const handleReview = (invoiceId: string) => {
    navigate(`/reviewer/invoice/${invoiceId}`);
  };

  const handleViewFile = (invoiceId: string, pdfUrl?: string) => {
    if (!pdfUrl) {
      return;
    }
    window.open(`${API_BASE_URL}/invoices/${invoiceId}/file`, '_blank', 'noopener,noreferrer');
  };

  const columns: Column<Invoice>[] = [
    {
      key: 'id',
      header: 'Invoice ID',
      render: (invoice) => (
        <span className="font-mono text-sm font-medium text-foreground">
          {invoice.id}
        </span>
      ),
    },
    {
      key: 'vendorName',
      header: 'Vendor Name',
      render: (invoice) => (
        <span className="font-medium text-foreground">{invoice.vendorName}</span>
      ),
    },
    {
      key: 'invoiceDate',
      header: 'Invoice Date',
      render: (invoice) => (
        <span className="text-muted-foreground">
          {format(new Date(invoice.invoiceDate), 'MMM d, yyyy')}
        </span>
      ),
    },
    {
      key: 'totalAmount',
      header: 'Amount',
      render: (invoice) => (
        <span className="font-medium text-foreground">
          ${invoice.totalAmount.toLocaleString('en-US', { minimumFractionDigits: 2 })}
        </span>
      ),
    },
    {
      key: 'status',
      header: 'Status',
      render: (invoice) => <StatusBadge status={invoice.status} />,
    },
    {
      key: 'actions',
      header: '',
      className: 'w-52',
      render: (invoice) => (
        <div className="flex items-center gap-2">
          <Button
            size="sm"
            variant="outline"
            disabled={!invoice.pdfUrl}
            onClick={(e) => {
              e.stopPropagation();
              handleViewFile(invoice.id, invoice.pdfUrl);
            }}
          >
            <ExternalLink className="w-4 h-4 mr-1" />
            File
          </Button>
          <Button
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              handleReview(invoice.id);
            }}
          >
            <Eye className="w-4 h-4 mr-1" />
            Review
          </Button>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <PageHeader 
        title="Review Queue" 
        description="Review and process pending invoices."
      />

      <Card className="shadow-card">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg">Pending Invoices</CardTitle>
          <CardDescription>
            {invoices?.length ?? 0} invoices waiting for review
          </CardDescription>
        </CardHeader>
        <CardContent>
          <DataTable
            data={invoices ?? []}
            columns={columns}
            keyExtractor={(invoice) => invoice.id}
            isLoading={isLoading}
            emptyMessage="No invoices in the queue"
            onRowClick={(invoice) => handleReview(invoice.id)}
          />
        </CardContent>
      </Card>
    </div>
  );
};

export default ReviewQueue;
