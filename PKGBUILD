# Maintainer: Your Name <your.email@example.com>

pkgname=routinely
pkgver=1.0.0
pkgrel=1
pkgdesc="A lightweight, open-source daily routine tracker"
arch=('any')
url="https://github.com/Unchain1014/Routinely"
license=('GPL3')
depends=('python-pyqt6')
makedepends=('git' 'python-pip' 'python')
source=("git+https://github.com/Unchain1014/Routinely")
sha256sums=('SKIP')

build() {
  cd "$srcdir/Routinely"
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  pip install pyinstaller
  pyinstaller --onefile src/main.py --name routinely
}

package() {
  cd "$srcdir/Routinely"
  install -D dist/routinely -t "$pkgdir/usr/bin/"
  install -D src/ui/icon.svg -t "$pkgdir/usr/share/icons/hicolor/scalable/apps/"
  install -Dm644 src/routinely.desktop -t "$pkgdir/usr/share/applications/"
}