# Email and Messaging

> See [Recipe Index](INDEX.md) for all recipes.

Model email messages and their metadata.

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.uco.observable import (
    ObservableObject, EmailMessageFacet, EmailAddressFacet,
)
from datetime import datetime

graph = CASEGraph()

sender = graph.create(ObservableObject,
    has_facet=[EmailAddressFacet(
        address_value="suspect@example.com",
        display_name="John Doe",
    )],
)

email = graph.create(ObservableObject,
    has_facet=[EmailMessageFacet(
        subject="Project Files",
        sent_time=datetime(2024, 3, 14, 16, 30, 0),
        is_read=True,
        content_type="text/plain",
        body="See attached files for the project deliverables.",
    )],
)

print(graph.serialize())
```

</details>

<details><summary>C#</summary>

```csharp
var graph = new CaseGraph();

graph.Add(new ObservableObject {
    HasFacet = { new EmailAddressFacet {
        AddressValue = "suspect@example.com",
        DisplayName = "John Doe"
    }}
});

graph.Add(new ObservableObject {
    HasFacet = { new EmailMessageFacet {
        Subject = "Project Files",
        SentTime = new DateTime(2024, 3, 14, 16, 30, 0),
        IsRead = true,
        ContentType = "text/plain",
        Body = "See attached files for the project deliverables."
    }}
});

Console.WriteLine(graph.Serialize());
```

</details>

<details><summary>Java</summary>

```java
CaseGraph graph = new CaseGraph();

var emailFacet = new EmailMessageFacet();
emailFacet.setSubject("Project Files");
emailFacet.setIsRead(true);
emailFacet.setBody("See attached files for the project deliverables.");
var emailObs = new ObservableObject();
emailObs.getHasFacet().add(emailFacet);
graph.add(emailObs);

System.out.println(graph.serialize());
```

</details>
