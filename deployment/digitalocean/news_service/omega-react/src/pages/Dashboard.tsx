import { Suspense } from 'react';
import Layout from '../components/layout/Layout';
import DashboardPage from '../components/dashboard/DashboardPage';
import LoadingSpinner from '../components/ui/LoadingSpinner';

const Dashboard = () => {
    return (
        <Layout>
            <Suspense fallback={<LoadingSpinner text="Loading dashboard..." />}>
                <DashboardPage />
            </Suspense>
        </Layout>
    );
};

export default Dashboard; 