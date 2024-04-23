#include <iostream>
#include <stdexcept>
#include <thread>
#include <chrono>
#include <mutex>
#include <random>
#include <math.h>
#include <iomanip>
using namespace std;

mutex myMutex;

// Want to calculate our local "inside" portion
// Then we try to see if the thread is locked
// if it ain't, we make global inside += local inside
void findInside(int& inside, int beg, int end, int thread_num) {
  int localInside = 0;

  // random function
  unsigned long milliseconds_since_epoch = std::chrono::system_clock::now().time_since_epoch() / std::chrono::milliseconds(1);
  unsigned long seed = milliseconds_since_epoch + (long) thread_num;
  mt19937 engine (seed);
  uniform_real_distribution<float> uniformDist(0.0, 1.0);

  for (auto i = beg; i < end; i++) {
    float x = uniformDist(engine);
    float y = uniformDist(engine);

    if(x*x + y*y <= 1.0) {
      localInside++;
    }
  }

  // Adding local sum where needed
  lock_guard<mutex> myLock(myMutex);
  inside += localInside;
}



int main(int argc, char *argv[]) {
  // First, we wanna check for two arguments passed in
  //
  // First argument: number of threads
  // Second argument: range of numbers (from 1 - n inclusive)
  try {
    // Argument exception handling
    if (argc < 3 or argc > 3) {
      throw runtime_error (
        "Please only pass in 2 arguments!"
      );
    }
    if ( stoi(argv[1]) < 0 || stoi(argv[1]) > 64 ) {
      throw runtime_error (
        "Please only have up to 64 threads!"
      );
    }
    
    // Extract arguments passed in 
    int number_of_threads = stoi(argv[1]);
    int total_points = stoi(argv[2]);
    
    // Generating how much slices are going to 
    int slice = floor((double)total_points / (double)number_of_threads);
    int startIndex = 0;

    // Global "inside" sum
    int inside = 0;

    thread t[number_of_threads];

    auto start = chrono::system_clock::now();
    // Starting the loop of threads
    for(int i = 0; i < number_of_threads; i++) {
      // In case the number of points / number of threads isn't nicely divisible, the last
      // thread is going to cover the whole range
      int endIndex = (i == number_of_threads - 1) ? total_points : startIndex + slice - 1;
      // I know it's working, so I don't want this anymore for 
      // cout << "Thread[" << i << "] - slice [" << startIndex << " : " << endIndex << "]" << endl;
      t[i] = thread(findInside, ref(inside), startIndex, endIndex, i);
      startIndex += slice;
    }

    for (int i = 0; i < number_of_threads; i++) {
      t[i].join();
    }

    double ans = (((double)inside * 4) / (double)total_points);
    chrono::duration<double> duration = chrono::system_clock::now() - start;
    cout << total_points << " ";
    cout << number_of_threads << " ";
    cout << ans << " ";
    cout << fixed << setprecision(6) << duration.count() << endl;

  } catch (const exception& e) {
	  cout << "Exception: " << e.what() << endl;
	  return 1;
  }
}
