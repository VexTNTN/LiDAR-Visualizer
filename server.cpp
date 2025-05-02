// server.cpp
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>

#include <chrono>
#include <cmath>
#include <cstring>
#include <iostream>
#include <thread>
#include <vector>

namespace {
constexpr uint16_t PORT = 12345;
constexpr double STEP = 0.04;
constexpr double X_START = -10.0;
constexpr double X_END = 10.0;
constexpr double MAX_SHIFT = 50.0;
constexpr double SHIFT_SPEED = 0.1;
constexpr int FPS = 60; // 1/75 s between frames

// Send all bytes in buf; return false on error/EOF.
bool send_all(int fd, const std::vector<std::uint8_t> &buf) {
  const std::uint8_t *p = buf.data();
  std::size_t rem = buf.size();
  while (rem) {
    ssize_t n = ::send(fd, p, rem, 0);
    if (n <= 0)
      return false; // error or peer closed
    p += n;
    rem -= static_cast<std::size_t>(n);
  }
  return true;
}
} // namespace

int main() {
  /* ---------- socket setup ------------------------------------------------ */
  int server_fd = ::socket(AF_INET, SOCK_STREAM, 0);
  if (server_fd == -1) {
    perror("socket");
    return 1;
  }

  // Allow quick rebinding after a crash/kill.
  int opt = 1;
  ::setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

  sockaddr_in addr{};
  addr.sin_family = AF_INET;
  addr.sin_addr.s_addr = INADDR_ANY;
  addr.sin_port = htons(PORT);

  if (::bind(server_fd, reinterpret_cast<sockaddr *>(&addr), sizeof(addr)) <
      0) {
    perror("bind");
    return 1;
  }
  std::cout << "socket binded to " << PORT << '\n';

  if (::listen(server_fd, 5) < 0) {
    perror("listen");
    return 1;
  }
  std::cout << "socket is listening\n";

  /* ---------- main accept loop ------------------------------------------- */
  for (;;) {
    sockaddr_in client{};
    socklen_t clen = sizeof(client);
    int cfd = ::accept(server_fd, reinterpret_cast<sockaddr *>(&client), &clen);
    if (cfd < 0) {
      perror("accept");
      continue;
    }
    std::cout << "Got connection\n";

    /* ---- greeting ----------------------------------------------------- */
    const char hello[] = "Thank you for connecting";
    // ::send(cfd, hello, sizeof(hello) - 1, 0);

    /* ---- streaming loop ---------------------------------------------- */
    double shift = 0.0;
    int dir = 1;
    while (true) {
      /* build payload ------------------------------------------------- */
      std::vector<short> shorts;
      shorts.reserve(1000); // 500 points × 2

      for (double x = X_START; x < X_END; x += STEP) {
        double xd = (x + shift);
        double yd = (std::sin(xd) * 50.0);
        short xs = floor(xd * 32767 / 72);
        short ys = floor(yd * 32767 / 72);
        std::cout << xs << std::endl;
        std::cout << ys << std::endl;
        shorts.push_back(xs);
        shorts.push_back(ys);
      }

      uint16_t count = static_cast<uint16_t>(shorts.size());
      uint16_t count_be = htons(count); // network order
      std::vector<std::uint8_t> packet(sizeof(count_be) +
                                       count * sizeof(short));
      // copy header + payload
      std::memcpy(packet.data(), &count_be, sizeof(count_be));
      std::memcpy(packet.data() + sizeof(count_be), shorts.data(),
                  shorts.size() * sizeof(short));

      /* send ---------------------------------------------------------- */
      if (!send_all(cfd, packet)) {
        std::cout << "Connection closed\n";
        break;
      }

      /* prepare next frame ------------------------------------------- */
      shift += SHIFT_SPEED * dir;
      if (shift > MAX_SHIFT || shift < -MAX_SHIFT)
        dir *= -1;

      std::this_thread::sleep_for(std::chrono::milliseconds(1000 / FPS));
    }
    ::close(cfd);
  }
  /* never reached */
}
