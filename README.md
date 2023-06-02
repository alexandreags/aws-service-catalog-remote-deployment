# aws-service-catalog-remote-deployment
Solução para deployments Remotos em linked Accounts usando Service Catalog

## Overview

Apesar do ServiceCatalog suportar o deployment para contas linked em ambientes com AWS Organizations Habilitado, não é possivel utilitar paremetros customizados para cada deployment. 

Essa solução usa um produto especifico dentro de um portfolio que usa Lambda e CF Custom resources para criar produtos provisionados nas contas das contas linkeds. 

Suporta a remoção de produtos provisionados. 

O deployment Centralizado concentra os produtos como versões do produto de deployment.
