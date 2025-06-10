# Wiki2Text

**Conversor de páginas Wiki (MediaWiki) a texto limpio.**

Proyecto en desarrollo.  
Este paquete permite extraer el contenido principal de páginas MediaWiki (por ejemplo Wikipedia) y convertirlo a texto limpio.

---

## Salida del text

/home/user/wiki2text/*


# Guía completa: cómo crear un ebuild con releases de GitBucket

1️⃣ Preparar el tag en Git

El ebuild usará un `.tar.gz` que se genera a partir de un **tag** en el repositorio Git.

Crear el tag:

git tag 1.0.0

git push origin 1.0.0

Esto hace que en GitBucket se genere el `.tar.gz` en la sección de "Releases" o en `/archive/`.

Borrar un tag (si hace falta):

Borrar local:

git tag -d 1.0.0

Borrar remoto (en GitBucket):

git push origin --delete 1.0.0

2️⃣ Buscar la URL del `.tar.gz`

Después de hacer el tag, entrar en GitBucket:

https://icae.intranet.gc/gitbucket/jrubioh/wiki2txt

Dar a crear Release

Ir a la pestaña de la Realease → copiar la URL del `.tar.gz`.

Ejemplo de URL válida:

https://icae.intranet.gc/gitbucket/jrubioh/wiki2txt/archive/1.0.0.tar.gz

3️⃣ Crear el ebuild

Nombre del ebuild:

<nombre>-<version>.ebuild

Esto dentro del path del repositorio ejemplo: /var/db/repos/overlayicae/*categoria*/*paquete*/*aqui*

Ejemplo:

wiki2txt-1.0.0.ebuild

Variables importantes en el ebuild:

PN: Nombre del paquete (por ejemplo: wiki2txt)
PV: Versión (por ejemplo: 1.0.0) — se saca del nombre del ebuild
P: ${PN}-${PV} → wiki2txt-1.0.0
WORKDIR: Directorio temporal de trabajo en /var/tmp/portage/...
DISTDIR: Directorio donde Portage guarda los `.tar.gz` descargados

Ejemplo de SRC_URI:

SRC_URI="https://icae.intranet.gc/gitbucket/jrubioh/wiki2txt/archive/${PV}.tar.gz -> ${P}.tar.gz"

Ejemplo de S (si hace falta):

Si el `.tar.gz` se descomprime como wiki2txt-1.0.0/, puedes poner:

S="${WORKDIR}/${P}"

Si se descomprime como wiki2txt-wiki2txt-1.0.0/, entonces:

S="${WORKDIR}/wiki2txt-wiki2txt-${PV}"

RESTRICT="mirror"

Para que Portage **no use mirrors de Gentoo** y siempre use la URL que tú pones:

RESTRICT="mirror"

Esto es **imprescindible** para ebuilds de repos internos (GitBucket).

Ejemplo completo de ebuild:

EAPI=8

PYTHON_COMPAT=( python3_{9..14} )

DESCRIPTION="Conversor de páginas Wiki (MediaWiki) a texto limpio."

DISTUTILS_USE_PEP517=poetry

#inherit distutils-r1 git-r3

inherit distutils-r1

SRC_URI="https://icae.intranet.gc/gitbucket/jrubioh/${PN}/archive/${PV}.tar.gz -> ${P}.tar.gz"

HOMEPAGE="https://icae.intranet.gc/gitbucket/jrubioh/${PN}"

#EGIT_REPO_URI="https://icae.intranet.gc/gitbucket/git/jrubioh/wiki2txt.git"

LICENSE="GPL-3"

SLOT="0"

KEYWORDS="~amd64 ~x86"

IUSE=""

RESTRICT="mirror" # para que vaya directamente a intranet sin intentar en repo Gentoo


REQUIRED_USE="${PYTHON_REQUIRED_USE}"

DISTUTILS_USE_SETUPTOOLS="rdepend"

RDEPEND="${PYTHON_DEPS}"

DEPEND="${RDEPEND}
dev-python/beautifulsoup4
dev-python/plumbum
dev-python/ply
dev-python/soupsieve
dev-python/termcolor
dev-python/tqdm
dev-python/setuptools
"

4️⃣ Cómo generar el Manifest

Cada vez que cambias:

El tag
La URL de SRC_URI
El `.tar.gz` subido
Debes **regenerar el Manifest por cada cambio o actulizacion de version, por cada version un ebuild**:

ebuild wiki2txt-1.0.0.ebuild manifest

Esto actualiza el `Manifest` con el checksum y tamaño actual del `.tar.gz`.

5️⃣ Dónde se descarga el `.tar.gz`

El `.tar.gz` se guarda en:

DISTDIR="/var/cache/distfiles"

Normalmente:

/var/cache/distfiles/wiki2txt-1.0.0.tar.gz

Borrar el `.tar.gz` si hay que forzar descarga nueva:

rm -f /var/cache/distfiles/wiki2txt-1.0.0.tar.gz

Borrar también el Manifest (si cambias la URL o si falla el checksum):

rm -f Manifest

6️⃣ Hacer el emerge:

emerge -av dev-python/wiki2txt

7️⃣ Resumen final:

Crear el tag en Git (git tag v1.0.0 → git push origin v1.0.0)
Copiar la URL del `.tar.gz`
Crear el ebuild con SRC_URI correcto
Poner RESTRICT="mirror"
Añadir S si hace falta
Regenerar Manifest
Borrar `.tar.gz` de cache si es necesario
Hacer emerge 🚀

Como esta en intranet y las deps ncesitan internet para instalarse lanzar emerge en inernet para que se instale las dep y cuado falle el principal, lanzar el emerger con --nodeps en intranet.
