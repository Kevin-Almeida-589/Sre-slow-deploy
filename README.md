🚀 SRE-Slow-Deploy

Este projeto é um laboratório de SRE (Site Reliability Engineering) focado em demonstrar um ciclo completo de CI/CD, Segurança em Containers e Escalabilidade Automática no Kubernetes.

A aplicação consiste em uma API Python que serve como base para testes de carga e automação de infraestrutura.
🛠️ Tecnologias Utilizadas

    Linguagem: Python 3.12 (FastAPI/Flask)

    Testes & Qualidade: Pytest, Pylint, Black

    Containerização: Docker

    Orquestração: Kubernetes (Minikube/Kind)

    HPA & Autoscaling: KEDA (Kubernetes Event-driven Autoscaling)

    Segurança: Trivy (Vulnerability Scanner)

    CI/CD: GitHub Actions

🏗️ Arquitetura do Pipeline

O fluxo de automação definido no .github/workflows/ci.yml segue as melhores práticas de DevSecOps:

    Job: PythonTests

        Instalação de dependências.

        Formatação de código com Black.

        Análise estática (Linting) com Pylint (Score mínimo: 9.0).

        Execução de testes unitários com Pytest.

    Job: Docker

        Build da imagem Docker utilizando tags baseadas no SHA do commit.

        Security Scan: Uso do Trivy para barrar o pipeline caso vulnerabilidades de nível HIGH ou CRITICAL sejam encontradas.

        Push para o Docker Hub.

    Job: Deploy (MiniKube)

        Provisionamento de ambiente Kubernetes.

        Instalação do Core do KEDA.

        Aplicação dos manifestos de /k8s.

        Atualização da imagem do Deployment (Rollout).

🚀 Como Executar
Pré-requisitos

    Docker instalado.

    Kubernetes (Minikube ou Kind).

    kubectl configurado.

Passo a Passo

    Clonar o repositório:
    Bash

    git clone https://github.com/Kevin-Almeida-589/Sre-slow-deploy.git
    cd Sre-slow-deploy

    Subir a infraestrutura local:
    Bash

    minikube start
    kubectl apply -f k8s/

    Verificar o Autoscaling (KEDA):
    O projeto utiliza o KEDA para escalar a aplicação. Verifique os ScaledObjects:
    Bash

    kubectl get scaledobjects

🛡️ Segurança e Qualidade

Para garantir a confiabilidade do sistema (Reliability), o projeto implementa:

    Gate de Qualidade: O pipeline falha se o código não seguir os padrões PEP8 ou se os testes falharem.

    Vulnerability Management: Imagens Docker são escaneadas em tempo de build.

    Resource Limits: Os manifestos K8s definem limites de CPU e Memória para evitar o "Noisy Neighbor effect".

📈 Próximos Passos (Roadmap SRE)

    [ ] Implementar métricas com Prometheus e Dashboards no Grafana.

    [ ] Adicionar Liveness e Readiness Probes para garantir o Self-healing.

    [ ] Configurar alertas de latência (SLIs/SLOs).

    [ ] Implementar Estratégia de Deploy Canary ou Blue/Green.

Desenvolvido por Kevin Almeida
