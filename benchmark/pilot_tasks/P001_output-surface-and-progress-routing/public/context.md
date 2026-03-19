# Environment
- terminal logger と chat relay が、同じ progress/debug event を共有している。
- 既存チェックは送信の有無や件数は見ても、どの面に何が出るかまでは見ていない。
- raw debug artifact を残すこと自体は許容されるが、ユーザー向けチャット面とは分ける必要がある。
