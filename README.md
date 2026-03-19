🛠️ Dark AutoKeyManager v1.0
O Dark AutoKeyManager é uma ferramenta de automação robusta desenvolvida por Darksider96 para facilitar o gerenciamento de servidores de DayZ Standalone. Com foco em produtividade e segurança, o software automatiza a sincronização de chaves de mods e a configuração de inicialização do servidor.

🚀 Funcionalidades
O software oferece dois modos de operação distintos para se adaptar à sua necessidade:

🏠 Servidor LOCAL
Sincronização de Keys: Varre todas as pastas de mods (ex: @TakistanPlus, @DBS_Magma) e copia automaticamente os arquivos .bikey para a pasta /keys raiz.

Limpeza Automática: Remove chaves órfãs de mods que não estão mais presentes, evitando conflitos de assinatura.

Atualização do start.bat: Utiliza Regex para localizar e atualizar a linha -mod= no seu arquivo de inicialização, mantendo-o sempre sincronizado com as pastas físicas do servidor.

🌐 Servidor ONLINE
Segurança de Chaves: Focado na integridade da pasta /keys, garantindo que apenas chaves de mods ativos permaneçam no diretório.

Preservação de Configurações: Não altera o start.bat, ideal para servidores que utilizam painéis de controle ou scripts de inicialização personalizados.

🎨 Interface e UX
Dark Mode Nativo: Interface moderna e confortável para longas sessões de desenvolvimento e manutenção.

Log em Tempo Real: Console integrado que exibe cada ação tomada pelo software (cópias, deleções e erros).

Independência de Ambiente: Versão executável que não requer a instalação do Python no servidor de destino.

🛠️ Como Usar
Coloque o executável DarkAutoKeyManager.exe na pasta raiz do seu servidor DayZ (onde fica o DayZServer_x64.exe).

Execute o programa.

Selecione o modo desejado (Local ou Online).

Clique em INICIAR AUTOMAÇÃO.

Confira o log de atividades e pronto! Seu servidor está higienizado e configurado.

💻 Desenvolvimento Técnico
Como um projeto derivado de uma abordagem de Full-Stack Development, o Dark AutoKeyManager foi construído utilizando:

Linguagem: Python 3.12.

GUI: Tkinter com customização de cores dark.

Processamento: Bibliotecas os, shutil e re para manipulação precisa de arquivos e strings.

Compilação: PyInstaller com suporte a recursos embutidos (_MEIPASS).

👤 Autor
Desenvolvido por Johnatan (Darksider96).
=======
Criador de soluções como DarkMonitor, Reino da Lógica e diversos mods para a comunidade DayZ (DBS Mods).
