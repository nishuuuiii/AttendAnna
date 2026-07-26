Adapted Use Case: Correctional Facility / Custodial Monitoring (Karnataka State Police Datathon 2026)

This project was originally built for classroom attendance (see above), but the core problem it solves — verifying someone is continuously present, not just present at a single checkpoint — extends directly to institutional and law-enforcement settings.

Problem in Custodial Settings

Traditional jail/custodial headcount systems rely on manual roll calls or one-time biometric checks (e.g. at a cell gate). A person can be accounted for at the checkpoint and be missing later — during transfers, work duty, or medical visits — with no way to detect the gap until the next scheduled roll call.

Adapted Solution — TRACKTHEM

Using the same continuous face-verification engine, the system tracks whether a registered individual (under-trial/inmate) remains detectable within a monitored zone throughout a defined time window. If continuous presence breaks before the threshold, it raises an immediate absence alert instead of waiting for the next manual check — closing the same "check-in and disappear" gap this project originally solved for classrooms.

What Changes for This Use Case
Registration → facility record (ID/cell block) instead of student roll number
Alert priority → absence triggers an immediate flag to duty staff, rather than just a logged "Present"/"Absent" entry
Planned integration → Zoho Catalyst (Data Store, Functions, Notifications) for multi-facility, production-scale deployment
Honest Status

This is a prototype-stage adaptation submitted for the Karnataka State Police Datathon 2026. The core face-verification pipeline is built and demoed (see demo video); custodial-specific features (liveness/anti-spoofing detection, multi-face detection, Catalyst backend) are on the roadmap, not yet implemented.