/**
 * Homepage - Public school website landing page.
 * (T074 - Implementation)
 */
import { Hero } from '../components/public/Hero';
import { PrincipalMessage } from '../components/public/PrincipalMessage';
import { NoticeBoard } from '../components/public/NoticeBoard';
import { TopStudentsSimple } from '../components/public/TopStudentsSimple';

export default function HomePage() {
  return (
    <>
      <Hero />

      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Principal Message - Takes 2 columns */}
          <div className="lg:col-span-2">
            <h2 className="text-3xl font-bold text-gray-800 mb-6">From the Principal's Desk</h2>
            <PrincipalMessage />
          </div>

          {/* Latest Notices - Takes 1 column */}
          <div>
            <div data-testid="latest-notices">
              <h2 className="text-3xl font-bold text-gray-800 mb-6">Latest Notices</h2>
              <NoticeBoard limit={3} />
              <a
                href="/notices"
                className="inline-block mt-4 text-blue-600 hover:text-blue-800 font-medium"
              >
                View All Notices →
              </a>
            </div>
          </div>
        </div>

        {/* Top Students Section */}
        <div className="mt-12">
          <TopStudentsSimple />
        </div>

        {/* Quick Links Section */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-4 gap-6">
          <a
            href="/faculty"
            className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg p-6 text-center transition-colors"
          >
            <h3 className="text-xl font-bold mb-2">Faculty</h3>
            <p className="text-sm">Meet our teachers</p>
          </a>
          <a
            href="/results"
            className="bg-green-600 hover:bg-green-700 text-white rounded-lg p-6 text-center transition-colors"
          >
            <h3 className="text-xl font-bold mb-2">Results</h3>
            <p className="text-sm">View exam results</p>
          </a>
          <a
            href="/gallery"
            className="bg-purple-600 hover:bg-purple-700 text-white rounded-lg p-6 text-center transition-colors"
          >
            <h3 className="text-xl font-bold mb-2">Gallery</h3>
            <p className="text-sm">School activities</p>
          </a>
          <a
            href="/notices"
            className="bg-orange-600 hover:bg-orange-700 text-white rounded-lg p-6 text-center transition-colors"
          >
            <h3 className="text-xl font-bold mb-2">Notices</h3>
            <p className="text-sm">Latest announcements</p>
          </a>
        </div>
      </div>
    </>
  );
}
