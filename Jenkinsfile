// =============================================================
// Pipeline declarativo — Curso Integración Continua · U2 / E4
// Etapas: pruebas dentro de un contenedor -> imagen Docker -> prueba de humo
// =============================================================
pipeline {
  agent none
  options {
    buildDiscarder(logRotator(numToKeepStr: '10'))
    timeout(time: 15, unit: 'MINUTES')
  }
  environment {
    IMAGEN = "inventario:${env.BUILD_NUMBER}"
  }
  stages {
    stage('Pruebas unitarias') {
      // Jenkins crea un contenedor efímero solo para esta etapa y lo elimina al final
      agent { docker { image 'python:3.12-slim' } }
      steps {
        sh '''
          python -m venv .venv
          . .venv/bin/activate
          pip install --quiet -r requirements-dev.txt
          pytest --junitxml=reportes/pruebas.xml
        '''
      }
      post {
        always { junit 'reportes/pruebas.xml' }
      }
    }
    stage('Construir imagen') {
      agent any
      steps {
        sh 'docker build -t $IMAGEN .'
      }
    }
    stage('Prueba de humo') {
      agent any
      steps {
        sh '''
          docker run -d --name humo-$BUILD_NUMBER $IMAGEN
          sleep 3
          docker exec humo-$BUILD_NUMBER python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/salud').read().decode())"
        '''
      }
      post {
        always { sh 'docker rm -f humo-$BUILD_NUMBER || true' }
      }
    }
  }
  post {
    success { echo "Build ${env.BUILD_NUMBER} OK: imagen ${env.IMAGEN} lista" }
    failure { echo 'El pipeline falló: revisa la etapa en rojo' }
  }
}
