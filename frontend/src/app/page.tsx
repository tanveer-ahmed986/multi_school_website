/**
 * Homepage - Public school website landing page.
 * Enhanced with Image Carousel and Principal Message
 */
import { Hero } from '../components/public/Hero';
import { PrincipalMessage } from '../components/public/PrincipalMessage';
import { NoticeBoard } from '../components/public/NoticeBoard';
import { ImageCarousel } from '../components/public/ImageCarousel';

export default function HomePage() {
  return (
    <>
      <Hero />

      <div className="container mx-auto px-4 py-12">
        {/* School Activities Carousel */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold text-gray-800 mb-6">
            🎓 School Life & Activities
          </h2>
          <ImageCarousel />
        </section>

        {/* Principal Message and Notices Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
          {/* Principal Message - Takes 2 columns */}
          <div className="lg:col-span-2">
            <h2 className="text-3xl font-bold text-gray-800 mb-6">
              👨‍💼 From the Principal's Desk
            </h2>
            <PrincipalMessage />
          </div>

          {/* Latest Notices - Takes 1 column */}
          <div>
            <div data-testid="latest-notices">
              <h2 className="text-3xl font-bold text-gray-800 mb-6">
                📢 Latest Notices
              </h2>
              <NoticeBoard limit={3} />
              <a
                href="/notices"
                className="inline-block mt-4 text-blue-600 hover:text-blue-800 font-medium transition-colors"
              >
                View All Notices →
              </a>
            </div>
          </div>
        </div>

        {/* Quick Links Section */}
        <section className="mt-16">
          <h2 className="text-3xl font-bold text-gray-800 mb-6 text-center">
            Quick Access
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <a
              href="/faculty"
              className="bg-gradient-to-br from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-lg p-6 text-center transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1"
            >
              <div className="text-4xl mb-2">👨‍🏫</div>
              <h3 className="text-xl font-bold mb-2">Faculty</h3>
              <p className="text-sm opacity-90">Meet our teachers</p>
            </a>
            <a
              href="/results"
              className="bg-gradient-to-br from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white rounded-lg p-6 text-center transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1"
            >
              <div className="text-4xl mb-2">📈</div>
              <h3 className="text-xl font-bold mb-2">Results</h3>
              <p className="text-sm opacity-90">View exam results</p>
            </a>
            <a
              href="/gallery"
              className="bg-gradient-to-br from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white rounded-lg p-6 text-center transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1"
            >
              <div className="text-4xl mb-2">🖼️</div>
              <h3 className="text-xl font-bold mb-2">Gallery</h3>
              <p className="text-sm opacity-90">School activities</p>
            </a>
            <a
              href="/notices"
              className="bg-gradient-to-br from-orange-600 to-orange-700 hover:from-orange-700 hover:to-orange-800 text-white rounded-lg p-6 text-center transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1"
            >
              <div className="text-4xl mb-2">📣</div>
              <h3 className="text-xl font-bold mb-2">Notices</h3>
              <p className="text-sm opacity-90">Latest announcements</p>
            </a>
          </div>
        </section>
      </div>
    </>
  );
}
